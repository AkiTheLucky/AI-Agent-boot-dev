from functions.get_files_info import get_files_info


if __name__ == "__main__":
    
    #test 1
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    
    #test 2
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)
    #test 3
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    #test 4
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)