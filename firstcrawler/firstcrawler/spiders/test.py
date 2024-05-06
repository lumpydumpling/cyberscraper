keywords = ["hi", "hello", "test", "test1"]

text_content = "temp, protest, spider, hello"

found_element = [keyword for keyword in keywords if ' ' + keyword in text_content]
print(found_element)