import os
import random
import copy
import logging
import csv
import json
import numpy as np
import torch
from transformers import (
    BertConfig,
    BertTokenizer,
)
import torch
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from tqdm import tqdm, trange
from transformers import AdamW, get_linear_schedule_with_warmup
import torch
import torch.nn as nn
from transformers import (BertModel, BertPreTrainedModel)
import logging
import argparse
import logging


class InputExample(object):
    """
    Un seul exemple de train / test pour une classification simple des séquences.

    Args:
        guid: Identifiant pour l'exemple.
        text_a: string. Le texte non tokenisé de la première séquence. Pour les séquences seules,
        seule cette séquence doit être spécifiée.
        label
    """

    def __init__(self, guid, text_a, label):
        self.guid = guid
        self.text_a = text_a
        self.label = label

    def __repr__(self):
        return str(self.to_json_string())

    def to_dict(self):
        output = copy.deepcopy(self.__dict__)
        return output

    def to_json_string(self):
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


class InputFeatures(object):
    """
    Un seul ensemble de features de données.

    Args:
        input_ids: Indices de la séquence d'entrée.
        attention_mask: Masque pour éviter d'appliquer de l'attention sur les tokens de padding.
            Valeur de masque sont ``[0, 1]``:
            ``1`` pour les tokens qui ne sont pas masqués, ``0`` pour les tokens masqués.
        token_type_ids: Index de token de segment pour indiquer la première et la deuxième partie des entrées.
    """

    def __init__(
            self, input_ids, attention_mask, token_type_ids, label_id, e1_mask, e2_mask
    ):
        self.input_ids = input_ids
        self.attention_mask = attention_mask
        self.token_type_ids = token_type_ids
        self.label_id = label_id
        self.e1_mask = e1_mask
        self.e2_mask = e2_mask

    def __repr__(self):
        return str(self.to_json_string())

    def to_dict(self):
        output = copy.deepcopy(self.__dict__)
        return output

    def to_json_string(self):
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


class process_dataset(object):
    """Processeur pour le dataset """

    def __init__(self, args):
        self.args = args
        self.relation_labels = get_label(args)

    @classmethod
    def _read_tsv(cls, input_file, quotechar=None):
        with open(input_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
            lines = []
            for line in reader:
                lines.append(line)
            return lines

    def _create_examples(self, lines, set_type):
        examples = []
        for (i, line) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            text_a = line[1]
            label = self.relation_labels.index(line[0])
            if i % 1000 == 0:
                logger.info(line)
            examples.append(InputExample(guid=guid, text_a=text_a, label=label))
        return examples

    def get_examples(self, mode):
        """
        Args:
            mode: train, dev, test
        """
        file_to_read = None
        if mode == "train":
            file_to_read = self.args.train_file
        elif mode == "dev":
            file_to_read = self.args.dev_file
        elif mode == "test":
            file_to_read = self.args.test_file

        logger.info(
            "LOOKING AT {}".format(os.path.join(self.args.data_dir, file_to_read))
        )
        return self._create_examples(
            self._read_tsv(os.path.join(self.args.data_dir, file_to_read)), mode
        )


def convert_examples_to_features(
        examples,
        max_seq_len,
        tokenizer,
        cls_token="[CLS]",
        cls_token_segment_id=0,
        sep_token="[SEP]",
        pad_token=0,
        pad_token_segment_id=0,
        sequence_a_segment_id=0,
        add_sep_token=False,
        mask_padding_with_zero=True,
):
    features = []
    for (ex_index, example) in enumerate(examples):
        if ex_index % 5000 == 0:
            logger.info("Writing example %d of %d" % (ex_index, len(examples)))

        tokens_a = tokenizer.tokenize(example.text_a)

        if "<e1>" not in tokens_a:
            break
        e11_p = tokens_a.index("<e1>")
        e12_p = tokens_a.index("</e1>")
        e21_p = tokens_a.index("<e2>")
        e22_p = tokens_a.index("</e2>")
        # Remplace le token
        tokens_a[e11_p] = "$"
        tokens_a[e12_p] = "$"
        tokens_a[e21_p] = "#"
        tokens_a[e22_p] = "#"

        # Ajoute 1 à cause du token [CLS]
        e11_p += 1
        e12_p += 1
        e21_p += 1
        e22_p += 1

        # Prend en compte [CLS] et [SEP] avec "- 2".
        if add_sep_token:
            special_tokens_count = 2
        else:
            special_tokens_count = 1
        if len(tokens_a) > max_seq_len - special_tokens_count:
            tokens_a = tokens_a[: (max_seq_len - special_tokens_count)]

        tokens = tokens_a
        if add_sep_token:
            tokens += [sep_token]

        token_type_ids = [sequence_a_segment_id] * len(tokens)

        tokens = [cls_token] + tokens
        token_type_ids = [cls_token_segment_id] + token_type_ids

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        attention_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        padding_length = max_seq_len - len(input_ids)
        input_ids = input_ids + ([pad_token] * padding_length)
        attention_mask = attention_mask + (
                [0 if mask_padding_with_zero else 1] * padding_length
        )
        token_type_ids = token_type_ids + ([pad_token_segment_id] * padding_length)

        e1_mask = [0] * len(attention_mask)
        e2_mask = [0] * len(attention_mask)

        for i in range(e11_p, e12_p + 1):
            e1_mask[i] = 1
        for i in range(e21_p, e22_p + 1):
            e2_mask[i] = 1

        assert len(input_ids) == max_seq_len, "Error with input length {} vs {}".format(
            len(input_ids), max_seq_len
        )
        assert (
                len(attention_mask) == max_seq_len
        ), "Error with attention mask length {} vs {}".format(
            len(attention_mask), max_seq_len
        )
        assert (
                len(token_type_ids) == max_seq_len
        ), "Error with token type length {} vs {}".format(
            len(token_type_ids), max_seq_len
        )

        label_id = int(example.label)
        # if ex_index < 5:
        #     print("*** Example ***")
            # print("guid: %s" % example.guid)
            # print("tokens: %s" % " ".join([str(x) for x in tokens]))
            # print("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            # print(
            #     "attention_mask: %s" % " ".join([str(x) for x in attention_mask])
            # )
            # print(
            #     "token_type_ids: %s" % " ".join([str(x) for x in token_type_ids])
            # )
            # print("label: %s (id = %d)" % (example.label, label_id))
            # print("e1_mask: %s" % " ".join([str(x) for x in e1_mask]))
            # print("e2_mask: %s" % " ".join([str(x) for x in e2_mask]))

        features.append(
            InputFeatures(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
                label_id=label_id,
                e1_mask=e1_mask,
                e2_mask=e2_mask,
            )
        )

    return features


def init_logger():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )


def load_tokenizer(args):
    tokenizer = MODEL_CLASSES[args.model_type][2].from_pretrained(
        args.model_name_or_path
    )
    tokenizer.add_special_tokens(
        {"additional_special_tokens": ADDITIONAL_SPECIAL_TOKENS}
    )
    return tokenizer


def load_and_cache_examples(args, tokenizer, mode):
    processor = processors[args.task](args)

    cached_features_file = os.path.join(
        args.data_dir,
        "cached_{}_{}_{}_{}".format(
            mode,
            args.task,
            list(filter(None, args.model_name_or_path.split("/"))).pop(),
            args.max_seq_len,
        ),
    )

    if os.path.exists(cached_features_file):
        features = torch.load(cached_features_file)
    else:
        if mode == "train":
            examples = processor.get_examples("train")
        elif mode == "dev":
            examples = processor.get_examples("dev")
        elif mode == "test":
            examples = processor.get_examples("test")
        else:
            raise Exception("Seulement train, dev, test est possible")

        features = convert_examples_to_features(
            examples, args.max_seq_len, tokenizer, add_sep_token=args.add_sep_token
        )
        torch.save(features, cached_features_file)

    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_attention_mask = torch.tensor(
        [f.attention_mask for f in features], dtype=torch.long
    )
    all_token_type_ids = torch.tensor(
        [f.token_type_ids for f in features], dtype=torch.long
    )
    all_e1_mask = torch.tensor(
        [f.e1_mask for f in features], dtype=torch.long
    )  # ajout masque e1
    all_e2_mask = torch.tensor(
        [f.e2_mask for f in features], dtype=torch.long
    )  # ajout masque e2

    all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.long)

    dataset = TensorDataset(
        all_input_ids,
        all_attention_mask,
        all_token_type_ids,
        all_label_ids,
        all_e1_mask,
        all_e2_mask,
    )
    return dataset




class FCLayer(nn.Module):
    def __init__(self, input_dim, output_dim, dropout_rate=0., use_activation=True):
        super(FCLayer, self).__init__()
        self.use_activation = use_activation
        self.dropout = nn.Dropout(dropout_rate)
        self.linear = nn.Linear(input_dim, output_dim)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.dropout(x)
        if self.use_activation:
            x = self.tanh(x)
        return self.linear(x)


class RBERT(BertPreTrainedModel):
    def __init__(self, config, args):
        super(RBERT, self).__init__(config)
        self.bert = PRETRAINED_MODEL_MAP[args.model_type](config=config)  # Load pretrained bert

        self.num_labels = config.num_labels

        self.cls_fc_layer = FCLayer(config.hidden_size, config.hidden_size, args.dropout_rate)
        self.e1_fc_layer = FCLayer(config.hidden_size, config.hidden_size, args.dropout_rate)
        self.e2_fc_layer = FCLayer(config.hidden_size, config.hidden_size, args.dropout_rate)
        self.label_classifier = FCLayer(config.hidden_size * 3, config.num_labels, args.dropout_rate, use_activation=False)

    @staticmethod
    def entity_average(hidden_output, e_mask):
        e_mask_unsqueeze = e_mask.unsqueeze(1)  # [b, 1, j-i+1]
        length_tensor = (e_mask != 0).sum(dim=1).unsqueeze(1)  # [batch_size, 1]

        sum_vector = torch.bmm(e_mask_unsqueeze.float(), hidden_output).squeeze(1)  # [b, 1, j-i+1] * [b, j-i+1, dim] = [b, 1, dim] -> [b, dim]
        avg_vector = sum_vector.float() / length_tensor.float()
        return avg_vector

    def forward(self, input_ids, attention_mask, token_type_ids, labels, e1_mask, e2_mask):
        outputs = self.bert(input_ids, attention_mask=attention_mask,
                            token_type_ids=token_type_ids)  # sequence_output, pooled_output, (hidden_states), (attentions)
        sequence_output = outputs[0]
        pooled_output = outputs[1]  # [CLS]

        # Average
        e1_h = self.entity_average(sequence_output, e1_mask)
        e2_h = self.entity_average(sequence_output, e2_mask)

        # Dropout -> tanh -> fc_layer
        pooled_output = self.cls_fc_layer(pooled_output)
        e1_h = self.e1_fc_layer(e1_h)
        e2_h = self.e2_fc_layer(e2_h)

        # Concat -> fc_layer
        concat_h = torch.cat([pooled_output, e1_h, e2_h], dim=-1)
        logits = self.label_classifier(concat_h)

        outputs = (logits,) + outputs[2:]

        # Softmax
        if labels is not None:
            if self.num_labels == 1:
                loss_fct = nn.MSELoss()
                loss = loss_fct(logits.view(-1), labels.view(-1))
            else:
                loss_fct = nn.CrossEntropyLoss()
                loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))

            outputs = (loss,) + outputs

        return outputs  # (loss), logits, (hidden_states), (attentions)
from sklearn.metrics import f1_score
def get_label(args):
    return [
        label.strip()
        for label in open(
            os.path.join(args.data_dir, args.label_file), "r", encoding="utf-8"
        )
    ]

def write_prediction(args, output_file, preds):
    relation_labels = get_label(args)
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, pred in enumerate(preds):
            f.write("{}\t{}\n".format(8001 + idx, relation_labels[pred]))

def compute_metrics(preds, labels):
    assert len(preds) == len(labels)
    return acc_and_f1(preds, labels)



def simple_accuracy(preds, labels):
    return (preds == labels).mean()


def acc_and_f1(preds, labels, average="macro"):
    acc = simple_accuracy(preds, labels)
    f1 = f1_score(preds, labels, average="micro")
    return {
        "acc": acc,
        "f1": f1,
    }


class Trainer(object):
    def __init__(self, args, train_dataset=None, dev_dataset=None, test_dataset=None):
        self.args = args
        self.train_dataset = train_dataset
        self.dev_dataset = dev_dataset
        self.test_dataset = test_dataset

        self.label_lst = get_label(args)

        self.num_labels = len(self.label_lst)

        self.config_class, self.model_class, _ = MODEL_CLASSES[args.model_type]
        self.config = self.config_class.from_pretrained(
            args.model_name_or_path,
            num_labels=self.num_labels,
            finetuning_task=args.task,
        )
        self.model = self.model_class.from_pretrained(
            args.model_name_or_path, config=self.config, args=args
        )

        # GPU or CPU
        self.device = (
            # "cpu"
            "cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu"
        )
        self.model.to(self.device)

    def train(self):
        train_sampler = RandomSampler(self.train_dataset)
        train_dataloader = DataLoader(
            self.train_dataset,
            sampler=train_sampler,
            batch_size=self.args.train_batch_size,
        )

        if self.args.max_steps > 0:
            t_total = self.args.max_steps
            self.args.num_train_epochs = (
                    self.args.max_steps
                    // (len(train_dataloader) // self.args.gradient_accumulation_steps)
                    + 1
            )
        else:
            t_total = (
                    len(train_dataloader)
                    // self.args.gradient_accumulation_steps
                    * self.args.num_train_epochs
            )

        # Prepare optimizer and schedule (linear warmup and decay)
        no_decay = ["bias", "LayerNorm.weight"]
        optimizer_grouped_parameters = [
            {
                "params": [
                    p
                    for n, p in self.model.named_parameters()
                    if not any(nd in n for nd in no_decay)
                ],
                "weight_decay": self.args.weight_decay,
            },
            {
                "params": [
                    p
                    for n, p in self.model.named_parameters()
                    if any(nd in n for nd in no_decay)
                ],
                "weight_decay": 0.0,
            },
        ]
        optimizer = AdamW(
            optimizer_grouped_parameters,
            lr=self.args.learning_rate,
            eps=self.args.adam_epsilon,
        )
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.args.warmup_steps,
            num_training_steps=t_total,
        )

        global_step = 0
        tr_loss = 0.0
        self.model.zero_grad()

        train_iterator = trange(int(self.args.num_train_epochs), desc="Epoch")
        loss_train = []
        for _ in train_iterator:
            epoch_iterator = tqdm(train_dataloader, desc="Iteration")
            for step, batch in enumerate(epoch_iterator):
                self.model.train()
                batch = tuple(t.to(self.device) for t in batch)  # GPU or CPU

                inputs = {
                    "input_ids": batch[0],
                    "attention_mask": batch[1],
                    "token_type_ids": batch[2],
                    "labels": batch[3],
                    "e1_mask": batch[4],
                    "e2_mask": batch[5],
                }

                outputs = self.model(**inputs)
                loss = outputs[0]

                if self.args.gradient_accumulation_steps > 1:
                    loss = loss / self.args.gradient_accumulation_steps

                loss.backward()
                loss_train.append(loss.item())
                tr_loss += loss.item()
                if (step + 1) % self.args.gradient_accumulation_steps == 0:
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(), self.args.max_grad_norm
                    )

                    optimizer.step()
                    scheduler.step()  # Update learning rate schedule
                    self.model.zero_grad()
                    global_step += 1

                    if (
                            self.args.logging_steps > 0
                            and global_step % self.args.logging_steps == 0
                    ):
                        self.evaluate("test")

                    if (
                            self.args.save_steps > 0
                            and global_step % self.args.save_steps == 0
                    ):
                        self.save_model()

                if 0 < self.args.max_steps < global_step:
                    epoch_iterator.close()
                    break

            if 0 < self.args.max_steps < global_step:
                train_iterator.close()
                break

        return global_step, tr_loss / global_step, loss_train

    def evaluate(self, mode):
        # We use test dataset because semeval doesn't have dev dataset
        if mode == "test":
            dataset = self.test_dataset
        elif mode == "dev":
            dataset = self.dev_dataset
        else:
            raise Exception("Only dev and test dataset available")

        eval_sampler = SequentialSampler(dataset)
        eval_dataloader = DataLoader(
            dataset, sampler=eval_sampler, batch_size=self.args.eval_batch_size
        )

        # Eval!
        print("***** Running evaluation on %s dataset *****", mode)
        print("  Num examples = %d", len(dataset))
        print("  Batch size = %d", self.args.eval_batch_size)
        eval_loss = 0.0
        nb_eval_steps = 0
        preds = None
        out_label_ids = None

        self.model.eval()
        loss_eval = []
        for batch in tqdm(eval_dataloader, desc="Evaluating"):
            batch = tuple(t.to(self.device) for t in batch)
            with torch.no_grad():
                inputs = {
                    "input_ids": batch[0],
                    "attention_mask": batch[1],
                    "token_type_ids": batch[2],
                    "labels": batch[3],
                    "e1_mask": batch[4],
                    "e2_mask": batch[5],
                }
                outputs = self.model(**inputs)
                tmp_eval_loss, logits = outputs[:2]

                eval_loss += tmp_eval_loss.mean().item()
                loss_eval.append(tmp_eval_loss.mean().item())
            nb_eval_steps += 1

            if preds is None:
                preds = logits.detach().cpu().numpy()
                out_label_ids = inputs["labels"].detach().cpu().numpy()
            else:
                preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)
                out_label_ids = np.append(
                    out_label_ids, inputs["labels"].detach().cpu().numpy(), axis=0
                )

        eval_loss = eval_loss / nb_eval_steps
        results = {"loss": eval_loss}
        preds = np.argmax(preds, axis=1)
        write_prediction(
            self.args, os.path.join(self.args.eval_dir, "lyz_proposed_answers.txt"), preds
        )

        result = compute_metrics(preds, out_label_ids)
        results.update(result)

        # print("***** Eval results *****")
        # for key in sorted(results.keys()):
        #     print("  {} = {:.4f}".format(key, results[key]))

        return results, loss_eval, preds, out_label_ids

    def save_model(self):
        # Save model checkpoint (Overwrite)
        if not os.path.exists(self.args.model_dir):
            os.makedirs(self.args.model_dir)
        model_to_save = (
            self.model.module if hasattr(self.model, "module") else self.model
        )
        model_to_save.save_pretrained(self.args.model_dir)

        # Save training arguments together with the trained model
        torch.save(self.args, os.path.join(self.args.model_dir, "training_args.bin"))
        logger.info("Saving model checkpoint to %s", self.args.model_dir)

    def load_model(self):
        # Check whether model exists
        if not os.path.exists(self.args.model_dir):
            raise Exception("Model doesn't exists! Train first!")

        try:
            self.args = torch.load(
                os.path.join(self.args.model_dir, "training_args.bin")
            )
            self.config = self.config_class.from_pretrained(self.args.model_dir)
            self.model = self.model_class.from_pretrained(
                self.args.model_dir, config=self.config, args=self.args
            )
            self.model.to(self.device)
            logger.info("***** Model Loaded *****")
        except:
            raise Exception("Some model files might be missing...")
csv_path = "E:\\File\\1_InnovateProj\\Algorithm\\RE\\eval\\flag.tsv"
if os.path.exists(csv_path):
    os.remove(csv_path)
processors = {"semeval": process_dataset}
ADDITIONAL_SPECIAL_TOKENS = ["<e1>", "</e1>", "<e2>", "</e2>"]
PRETRAINED_MODEL_MAP = {
    'bert': BertModel,
}
MODEL_CLASSES = {
    "bert": (BertConfig, RBERT, BertTokenizer),
}
MODEL_PATH_MAP = {
    "bert": "bert-base-uncased",
}
logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()

parser.add_argument(
    "--task", default="semeval", type=str, help="The name of the task to train"
)
parser.add_argument(
    "--data_dir",
    default="./data_RE/test",
    type=str,
    help="The input data dir. Should contain the .tsv files (or other data files) for the task.",
)
parser.add_argument(
    "--model_dir", default="./model", type=str, help="Path to model"
)
parser.add_argument(
    "--eval_dir",
    default="./eval",
    type=str,
    help="Evaluation script, result directory",
)
parser.add_argument(
    "--train_file", default="train.tsv", type=str, help="Train file"
)
parser.add_argument("--test_file", default="lyz_test.tsv", type=str, help="Test file")
parser.add_argument(
    "--label_file", default="label.txt", type=str, help="Label file"
)

parser.add_argument(
    "--model_type",
    default="bert",
    type=str,
    help="Model type selected in the list: " + ", ".join(MODEL_CLASSES.keys()),
)

parser.add_argument(
    "--seed", type=int, default=42, help="random seed for initialization"
)
parser.add_argument(
    "--train_batch_size", default=16, type=int, help="Batch size for training."
)
parser.add_argument(
    "--eval_batch_size", default=32, type=int, help="Batch size for evaluation."
)
parser.add_argument(
    "--max_seq_len",
    default=384,
    type=int,
    help="The maximum total input sequence length after tokenization.",
)
parser.add_argument(
    "--learning_rate",
    default=0.0001,
    type=float,
    help="The initial learning rate for Adam.",
)
parser.add_argument(
    "--num_train_epochs",
    default=5.0,
    type=float,
    help="Total number of training epochs to perform.",
)
parser.add_argument(
    "--weight_decay", default=0.0, type=float, help="Weight decay if we apply some."
)
parser.add_argument(
    "--gradient_accumulation_steps",
    type=int,
    default=1,
    help="Number of updates steps to accumulate before performing a backward/update pass.",
)
parser.add_argument(
    "--adam_epsilon", default=0.00001, type=float, help="Epsilon for Adam optimizer."
)
parser.add_argument(
    "--max_grad_norm", default=1.0, type=float, help="Max gradient norm."
)
parser.add_argument(
    "--max_steps",
    default=-1,
    type=int,
    help="If > 0: set total number of training steps to perform. Override num_train_epochs.",
)
parser.add_argument(
    "--warmup_steps", default=0, type=int, help="Linear warmup over warmup_steps."
)
parser.add_argument(
    "--dropout_rate",
    default=0.1,
    type=float,
    help="Dropout for fully-connected layers",
)

parser.add_argument(
    "--logging_steps", type=int, default=250, help="Log every X updates steps."
)
parser.add_argument(
    "--save_steps",
    type=int,
    default=250,
    help="Save checkpoint every X updates steps.",
)

parser.add_argument(
    "--do_train", action="store_true", help="Whether to run training."
)
parser.add_argument(
    "--do_eval", action="store_true", help="Whether to run eval on the test set."
)
parser.add_argument(
    "--no_cuda", action="store_true", help="Avoid using CUDA when available"
)
parser.add_argument(
    "--add_sep_token",
    action="store_true",
    help="Add [SEP] token at the end of the sentence",
)


args = parser.parse_args("")

args.model_name_or_path = MODEL_PATH_MAP[args.model_type]
tokenizer = load_tokenizer(args)

# Delete cache, or results will be same all the time.
cache_path = "E:\\File\\1_InnovateProj\\Algorithm\\RE\\data_RE/test/cached_test_semeval_bert-base-uncased_384"
if os.path.exists(cache_path):
    os.remove(cache_path)


test_dataset = load_and_cache_examples(args, tokenizer, mode="test")
trainer = Trainer(args, test_dataset=test_dataset)
args.do_eval = True
if args.do_eval:
    trainer.load_model()
    res, test_loss, preds, labels  = trainer.evaluate("test")

with open(csv_path, 'a', encoding='utf-8') as f1:
    f1.write("flag")
f1.close()