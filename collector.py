for i in range(1,25):
    with open('SERIALS/captions'+str(i)+'.txt','r',encoding='utf-8')as f,\
    open('final_captions.txt','a',encoding='utf-8')as x:
        content=f.readlines()
        x.write(''.join(content))
print('SUCCESS')