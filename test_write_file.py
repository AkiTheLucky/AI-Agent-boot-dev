from functions.write_files import write_file



if __name__ == "__main__":
    
    #test 1
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    
    print(result)
    
    #test 2
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    
    print(result)
    #test 3
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    
    print(result)

   