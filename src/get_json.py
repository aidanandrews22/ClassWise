from scraper import MathCoursesParser

input_files = ["math_courses.html", "phys_courses.html", "cs_courses.html"]
output_files = ["math_courses.json", "phys_courses.json", "cs_courses.json"]

i = 0
for file in input_files:
    parser = MathCoursesParser(file)
    parser.parse_courses()
    parser.save_to_json(output_files[i])
    i += 1

courses_data = parser.get_courses()
