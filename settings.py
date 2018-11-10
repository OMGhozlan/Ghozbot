import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
corp_dir = os.path.join(PROJECT_ROOT, 'Data', 'Corpus')
knbs_dir = os.path.join(PROJECT_ROOT, 'Data', 'KnowledgeBase')
res_dir = os.path.join(PROJECT_ROOT, 'Data', 'Result')