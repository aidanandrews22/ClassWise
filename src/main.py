# from sentence_transformers import util, SentenceTransformer
from UserNode import UserNode
import time
from typing import List


class Main:
    def __init__(
        self,
        user_id: str = "aidan",
        pdf_paths: List[str] = ["data/resume/Aidan_Andrews_Resume.pdf"],
    ):
        self.user_id = user_id
        self.pdf_paths = pdf_paths
        self.user = UserNode(user_id, pdf_paths)

    def main(self):
        return


start_time = time.time()
main = Main()
main.main()
end_time = time.time()
print(f"Time: {end_time - start_time}")
