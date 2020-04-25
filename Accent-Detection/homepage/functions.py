# # -*- coding: utf-8 -*-
# # import config

# def generate_dictionary(tag, max_word_length):
#     lst = []
#     for topic in config.language_tags[tag]:
#         content=topic
#         lst.append(content)

#     return lst

# def convert_dic_to_bin_vector(dic, max_word_length):
#     new_list = []
#     for word in dic:
#         vec = ""
#         n = len(word)
#         for i in range(n):
#             current_letter = word[i]
#             ind = ord(current_letter) - 2687
#             placeholder = bin(ind).replace("0b","")
#             if(len(placeholder) < 9):
#                 diff = 8 - len(placeholder)
#                 for i in range(diff):
#                     placeholder = "0" + placeholder
#             vec = vec + placeholder
#         if(len(vec) <= 128):
#             diff = 128 - len(vec)
#             for i in range(diff):
#                 vec = vec + "0"
#         new_list.append(vec)
#     return(new_list)

# def convert_dic_to_vector(dic, max_word_length):
#     new_list = []
#     for word in dic:
#         vec = ''
#         n = len(word)
#         for i in range(n):
#             current_letter = word[i]
#             ind = ord(current_letter)-2688
#             placeholder = (str(0)*ind) + str(1) + str(0)*(126-ind)
#             vec = vec + placeholder
#         if n < max_word_length:
#             excess = max_word_length-n
#             vec = vec +str(0)*127*excess
#         new_list.append(vec)
#     return new_list

# def create_output_vector(tag_index, number_of_languages):
#     out = str(0)*tag_index + str(1) + str(0)*(number_of_languages-1-tag_index)
#     return out