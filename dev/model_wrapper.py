import tika
import numpy as np
tika.initVM()
from tika import parser
import pickle
import eli5
import re
from nltk.corpus import stopwords
russian_stopwords = stopwords.words("russian")

def feature_filter(feature, i):
    return (feature not in russian_stopwords) and re.match(r'[^_]+', feature)

class Predictor(object):
    def __init__(self, model_path: str):
        self.id2label = ['Договоры аренды', 'Договоры купли-продажи',
                         'Договоры оказания услуг', 'Договоры подряда',
                         'Договоры поставки']
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)

    def predict_from_file(self, filepath: str) -> dict:
        text = Predictor._get_document_text(filepath)
        probas = self.model.predict_proba([text.lower()])[0]
        class_label = np.argmax(probas)
        return {'confidence': round(probas[class_label] * 100, 2),
                'class': self.id2label[class_label]}



    def write_html_markup(self, text, predicted_class, out_html_path='./out_html.html'):
        expl = eli5.ipython.explain_prediction(self.model['logisticregression'],
                                               text.lower(),
                                               vec=self.model['countvectorizer'],
                                               target_names=self.id2label,
                                               targets=[predicted_class],
                                               top=4,
                                               feature_filter=feature_filter)
        dict_expl = eli5.format_as_dict(expl)
        weights = [i[2] for i in dict_expl['targets'][0]['weighted_spans']['docs_weighted_spans'][0]['spans']]
        max_w = np.max(weights)
        min_w = np.min(weights)
        weights = [max(w - min_w, 0.5) / (max_w - min_w) for w in weights]

        span = dict_expl['targets'][0]['weighted_spans']['docs_weighted_spans'][0]['spans']
        html_template = text.lower()
        sum_shift = 0

        with open(out_html_path, 'w') as f:
            for idx, word in enumerate(span):
                span_start = word[1][0][0]
                span_end = word[1][0][1]
                o = weights[idx]
                shift = len(f'<span style="background-color:rgba(0, 255, 0, {o});"></span>')
                styled_word = f'<span style="background-color:rgba(0, 255, 0, {o});">{html_template[span_start + sum_shift:span_end + sum_shift]}</span>'
                html_template = html_template[:span_start + sum_shift] \
                                + styled_word \
                                + html_template[span_end + sum_shift:]

                sum_shift += shift
            html_template = html_template.replace('\n', '<br>').replace('\t', 'nbsp;')
            f.write(html_template)


    @staticmethod
    def _get_document_text(filepath: str) -> str:
        doc_type = filepath.split('.')[-1]
        if doc_type in ['doc', 'rtf', 'pdf', 'docx']:
            text = parser.from_file(filepath)['content']
        else:
            raise NotImplementedError(f'File extention must be either pdf, rtf, doc or docx, got {doc_type}')
        return text.strip()


pred = Predictor('baseline.pkl')

pred.predict_from_file('../data/xmas/docs/02682d726b725f95b9ee85f751c043d0.doc')
