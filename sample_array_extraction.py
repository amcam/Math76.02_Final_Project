import extract_array

big_array = extract_array.get_3d_array("M4ReconTomo.raw", "M4ReconTomo.dat")
shape = big_array.shape
print(f"The 3d array has {shape[0]} layers, {shape[1]} rows, and {shape[2]} columns!")
print(f"For example, the intensity value at layer 5, row 7, and column 112 is {big_array[5,7,112]}.\n(Note that we are starting index counting from 0)")
