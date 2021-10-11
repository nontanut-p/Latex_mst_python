from tkinter.filedialog import askopenfilenames

filenames = askopenfilenames(title="Open 'xls' or 'xlsx' file")

for filename in filenames:
    print(filename)
