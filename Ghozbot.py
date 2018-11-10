import os
import re
import settings
import sys
import tensorflow as tf
from Ghozpredictor import GhozPredictor



def Ghozbot():
    with tf.Session() as sess:
        predictor = GhozPredictor(sess, corpus_dir=settings.corp_dir, knbase_dir=settings.knbs_dir,
                                 result_dir=settings.res_dir, result_file='basic')
        # This command UI has a single chat session only
        session_id = predictor.session_data.add_session()

        print("Welcome to Chat with Ghozbot!")
        print("Type exit and press enter to end the conversation.")
        # Waiting from standard input.
        sys.stdout.write("> ")
        sys.stdout.flush()
        question = sys.stdin.readline()
        while question:
            if question.strip() == 'exit':
                print("Thank you for using Ghozbot. Goodbye.")
                break

            print(re.sub(r'_nl_|_np_', '\n', predictor.predict(session_id, question)).strip())
            print("> ", end="")
            sys.stdout.flush()
            question = sys.stdin.readline()

if __name__ == "__main__":
    Ghozbot()