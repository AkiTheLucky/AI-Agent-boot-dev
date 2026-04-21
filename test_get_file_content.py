from functions.get_file_content import get_file_content



if __name__ == "__main__":
    
    #test 1
    result = get_file_content("calculator", "lorem.txt")
    
    print(result)
    
    #test 2
    result = get_file_content("calculator", "main.py")
    
    print(result)
    #test 3
    result = get_file_content("calculator", "pkg/calculator.py")
    
    print(result)

    #test 4
    result = get_file_content("calculator", "/bin/cat")
    
    print(result)

    #test 5

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(result)