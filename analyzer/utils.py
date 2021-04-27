import numpy as np
import logging
import os

from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from mysite.settings import WordVec, graph
from tensorflow.keras.models import load_model

from analyzer.defaults import defaults
from analyzer.models import Attachment, Task

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

log = logging.getLogger(__name__)
STOP_WORDS = set(stopwords.words("english"))


def staff_check(user):
    """If STAFF_ONLY is set to True, limit view access to staff users only."""

    if defaults("STAFF_ONLY"):
        return user.is_staff
    else:
        # If unset or False, allow all logged in users
        return True


def user_can_read_task(task, user):
    return task.task_list.group in user.groups.all() or user.is_superuser


def toggle_task_checked(task_id: str) -> bool:
    """Toggle the `checked` bool on Task from True to False or vice versa."""
    try:
        task = Task.objects.get(id=task_id)
        task.checked = not task.checked
        task.save()
        return True

    except Task.DoesNotExist:
        log.info(f"Task {task_id} not found.")
        return False


def remove_attachment_file(attachment_id: int) -> bool:
    """Delete an Attachment object and its corresponding file from the filesystem."""
    try:
        attachment = Attachment.objects.get(id=attachment_id)
        if attachment.file:
            if os.path.isfile(attachment.file.path):
                os.remove(attachment.file.path)

        attachment.delete()
        return True

    except Attachment.DoesNotExist:
        log.info(f"Attachment {attachment_id} not found.")
        return False


def regex_tokenizer(sent):
    return RegexpTokenizer(r'\w+').tokenize(sent.lower())


def stopwords_elimination(stop_words, sent):
    return [w.lower() for w in sent if w.lower() not in stop_words]


def lemmatize_words(words):
    return [WordNetLemmatizer().lemmatize(word) for word in words]


def irr_words_elim(words):
    while True:
        ready = True

        for word in words:
            if word.isdigit() or len(word) <= 3:
                ready = False
                words.remove(word)

        if ready: break

    return words


def data_preparation(sent):
    words_list = regex_tokenizer(sent)
    words_list = stopwords_elimination(STOP_WORDS, words_list)
    words_list = lemmatize_words(words_list)
    words_list = irr_words_elim(words_list)

    return words_list


def sent_embed(words):
    sent_embed = []
    words_list = list(WordVec.vocab)

    for word in words:
        if word not in words_list:
            sent_embed.append([0] * 50)
        elif word in words_list:
            sent_embed.append(WordVec[word])

    return sent_embed


def fix_sentence_len(sentence, length):
    if len(sentence) > length:
        sentence = sentence[:length]
    elif len(sentence) < length:
        for i in range(length - len(sentence)):
            zeros = [0] * 50
            sentence.append(zeros)
    return sentence


def predict(sent):
    data = data_preparation(sent)
    data = sent_embed(data)
    data = fix_sentence_len(data, 100)
    data = np.reshape(data, (1, 100, 50))

    with graph.as_default():
        model = load_model("models/LSTM-Mini-Batch-Model.h5")  # load model
        print(model.predict(np.array(data)))
        return model.predict(np.array(data))


def convert_pdf_to_txt(path):
    rsrcmgr, retstr, laparams = PDFResourceManager(), StringIO(), LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password, maxpages, caching, pagenos = "", 0, True, set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text
