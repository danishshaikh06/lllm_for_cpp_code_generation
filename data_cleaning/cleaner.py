import re

input_file = "cpp_dataset.txt"
output_file = "cpp_dataset_clean.txt"

with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# remove large license blocks (/* ... */) longer than 200 characters
text = re.sub(r"/\*[\s\S]{200,}?\*/", "", text)

# remove repeated FILE_SEPARATOR gaps
text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("Clean dataset saved as:", output_file)
