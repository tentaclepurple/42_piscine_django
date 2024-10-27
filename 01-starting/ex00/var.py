def my_var():
    int_var = 42
    str_var_num = "42"
    str_var_text = "quarante-deux"
    float_var = 42.0
    bool_var = True
    list_var = [42]
    dict_var = {42: 42}
    tuple_var = (42,)
    set_var = set()

    print(f"{int_var} has a type {type(int_var)}")
    print(f"{str_var_num} has a type {type(str_var_num)}")
    print(f"{str_var_text} has a type {type(str_var_text)}")
    print(f"{float_var} has a type {type(float_var)}")
    print(f"{bool_var} has a type {type(bool_var)}")
    print(f"{list_var} has a type {type(list_var)}")
    print(f"{dict_var} has a type {type(dict_var)}")
    print(f"{tuple_var} has a type {type(tuple_var)}")
    print(f"{set_var} has a type {type(set_var)}")


if __name__ == '__main__':
    my_var()
