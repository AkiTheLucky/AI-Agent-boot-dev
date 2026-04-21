from functions.run_python_file import run_python_file



if __name__ == "__main__":
    
    #test 1
    result = run_python_file("calculator", "main.py")
    
    print(result)
    
    #test 2
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    
    print(result)
    #test 3
    result = run_python_file("calculator", "tests.py")
    
    print(result)

    #test 4
    result = run_python_file("calculator", "../main.py")
    
    print(result)
    
    #test 5
    result = run_python_file("calculator", "nonexistent.py")
    
    print(result)
    #test 6
    result = run_python_file("calculator", "lorem.txt")
    
    print(result)

   