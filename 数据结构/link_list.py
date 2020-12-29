def removeElement(phead,mink,maxk):
	p = phead
	while p:
		if(p.next.data>mink and p.next.data<maxk):
			tmp_point = p.next
			p.next = p.next.next
			del tmp_point
		else:
			p = p.next

def concat_link(ha,hb):
	p = ha
	while p.next:#找出第一个链表中最后一个元素的指针
		p = p.next
	p.next = hb.next
	return ha

def get_link_length(head):
	p = head
	count = 0
	while p.next:
		count += 1
		p = p.next
	return count

def get_index(phead,value):
	if(phead.next==None):
		print('空链表')
		return 0
	p = phead.next
	count = 0
	while p:
	 	if(p.data==value):
	 		return count
	 	else:
	 		count += 1
	 		p = p.next
	print('没有找到元素')
	return -1

def concat_orderly(fhead,shead,nhead):#nhead是一个新的链表的头指针
	p = fhead.next
	q = shead.next
	tmp_point = nhead#动态移动新链表的指针
	while p!=None and q!=None:
		if(p.data<q.data):
			tmp_point.next = p
			p = p.next
			tmp_point = tmp_point.next
		else:
			tmp_point.next = q
			q = q.next
			tmp_point = tmp_point.next
	if(p==None):#如果第一个链表为空,将第二个链表以后的元素直接连接到到新链表
		tmp_point = q
	if(q==None):#如果第二个链表为空,将第一个链表以后的元素直接连接到到新链表
		tmp_point = p
	return nhead

def invert(phead):
	p = phead
	q = None
	while p:
		r = q
		q = p
		p = p.next
		q.next = r
	return q

			

