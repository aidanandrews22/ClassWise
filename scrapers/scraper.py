import json
from bs4 import BeautifulSoup


class MathCoursesParser:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.courses = []

    def parse_courses(self):
        with open(self.input_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        for course_block in soup.find_all("div", class_="courseblock"):
            title_block = course_block.find("p", class_="courseblocktitle")
            desc_block = course_block.find("p", class_="courseblockdesc")

            if title_block and desc_block:
                course = self._extract_course_info(title_block, desc_block)
                self.courses.append(course)

    def _extract_course_info(self, title_block, desc_block):
        link = title_block.find("a", class_="schedlink")
        full_title = title_block.get_text(strip=True)

        # Extracting class number and title
        parts = full_title.split(maxsplit=3)
        class_number = f"{parts[0]} {parts[1]}"
        class_title = parts[2]

        # Extracting credits
        credits = ""
        if "credit:" in full_title:
            credits = full_title.split("credit:")[-1].strip()

        # Extracting description
        description = desc_block.get_text(strip=True)

        return {
            "class-number": class_number,
            "class-title": class_title,
            "credits": credits,
            "description": description,
            "link": link["href"] if link else "",
        }

    def save_to_json(self, output_file_path):
        with open(output_file_path, "w", encoding="utf-8") as file:
            json.dump(self.courses, file, indent=2, ensure_ascii=False)
        print(f"JSON file has been created: {output_file_path}")

    def get_courses(self):
        return self.courses


# Usage example:
if __name__ == "__main__":
    input_file = "math_courses.html"
    output_file = "math_courses.json"

    parser = MathCoursesParser(input_file)
    parser.parse_courses()
    parser.save_to_json(output_file)

    # If you want to work with the courses data in your script:
    courses_data = parser.get_courses()
    print(f"Parsed {len(courses_data)} courses.")
