import os

repo_folder = "repos"
output_file = "cpp_dataset.txt"

# C++ file extensions
extensions = [".cpp", ".cc", ".cxx", ".h", ".hpp"]

file_count = 0

with open(output_file, "w", encoding="utf-8") as outfile:

    for root, dirs, files in os.walk(repo_folder):

        for file in files:

            if any(file.endswith(ext) for ext in extensions):

                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()

                        outfile.write(code)
                        outfile.write("\n\n// FILE_SEPARATOR\n\n")

                        file_count += 1

                except:
                    pass

print("Total C++ files collected:", file_count)
print("Dataset saved as:", output_file)
