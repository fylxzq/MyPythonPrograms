class bintreeNode:
    def __init__(self):
        self.data = None
        self.lChild = None
        self.rChild = None
class teststr:
    def __init__(self):
        self.strs = ""
        self.index = 0

def createBinTree(strs):
    ch = strs.strs[strs.index:][0]
    strs.index +=1
    if (ch == '_'):
        head = None
    else:
        newnode = bintreeNode()
        newnode.data = ch
        head = newnode
        head.lChild = createBinTree(strs)
        head.rChild = createBinTree(strs)
    return head
def pretraverse(head):#前序遍历
    if(head!=None):
        print(head.data,end= " ")
        pretraverse(head.lChild)
        pretraverse(head.rChild)
def medtraverse(head):#中序遍历
    if(head!=None):
        medtraverse(head.lChild)
        print(head.data,end=" ")
        medtraverse(head.rChild)
def posttraverse(head):
    if(head!=None):
        posttraverse(head.lChild)
        posttraverse(head.rChild)
        print(head.data,end=" ")

def Judge(T1,T2):#判断是否镜像相同
    if(T1==None and T2 == None):
        return True
    if(T1 ==None or T2 ==None):
        return False
    if(T1.data==T2.data):
        return Judge(T1.lChild,T2.lChild) and Judge(T2.rChild,T2.rChild)
    else:
        return False

def main():
    s1 = teststr()
    s1.strs = "FAB__C__G__"
    T1 = createBinTree(s1)
    s2 = teststr()
    s2.strs = "FAB__C__G__"
    T2 = createBinTree(s2)
    print("T1前序遍历为:")
    pretraverse(T1)
    print()
    print("T2前序遍历为:")
    pretraverse(T2)
    print()
    flag = Judge(T1,T2)#判断是否相等或者镜像
    print("T1与T2是否相等或镜像:",flag)
main()


