def conc_path(cmd_list,param):
    path=""
    for i in range(cmd_list.index(param)+1,len(cmd_list)):
        path+=cmd_list[i]+" "
    del cmd_list[cmd_list.index(param)+1:len(cmd_list)]
    cmd_list.append(path[:-1])
    return cmd_list