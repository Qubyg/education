#include <stdio.h>
#include <stdlib.h>

//Определяем структуру блока односвязного списка
typedef struct Node {
	int value;         //данные 
	struct Node *next; //адрес следующего блока
}Node;

//добавление блока в начало
void push(Node **head, int data)
{
	Node *tmp = (Node*) malloc(sizeof(Node));
	tmp->value = data;
	tmp->next = (*head);
	(*head) = tmp;
}

//удаление начального блока
int pop(Node **head)
{
	Node* prev = NULL;
	int val;
	if(head == NULL)
	{
		exit(-1);
	}
	prev = (*head);
	val = prev->value;
	(*head) = (*head)->next;
	free(prev);
	return val;
}

//получение адреса n-ого блока
Node* getNth(Node* head, int n)
{
	int counter = 0;
	while(counter < n && head)
	{
		head = head->next;
		counter++;
	}
	return head;
}

//получение адреса последнего блока
Node* getLast(Node *head)
{
	if(head == NULL)
	{
		return NULL;
	}
	while (head->next)
	{
		head = head->next;
	}
	return head;
}

//добавление блока в конец 
void pushBack(Node *head, int value)
{
	Node *last = getLast(head);
	Node *tmp = (Node*) malloc(sizeof(Node));
	tmp->value = value;
	tmp->next = NULL;
	last->next = tmp;
}

//получение адреса предпоследнего блока
Node* getLastButOne(Node *head)
{
	if(head == NULL)
	{
		exit(-2);
	}
	if(head->next == NULL)
	{
		return NULL;
	}
	while(head->next->next)
	{
		head = head->next;
	}
	return head;
	
}

//удадение последнего блока
void popBack(Node **head)
{
	Node *lastbn = NULL;
	if (!head)
	{
		exit(-1);
	}
	if (!(*head))
	{
		exit(-1);
	}
	lastbn = getLastButOne(*head);
	if (lastbn == NULL)
	{
		free(*head);
		*head = NULL;
	} else {
		free(lastbn->next);
		lastbn->next = NULL;
	}
}

//вствка блока в n-ое место
void insert(Node *head, unsigned n, int val)
{
	unsigned i = 0;
	Node *tmp = NULL;
	while (i < n && head->next)
	{
		head = head->next;
		i++;
	}
	tmp = (Node*) malloc(sizeof(Node));
	tmp->value = val;
	if (head->next)
	{
		tmp->next = head->next;
	} else {
		tmp->next = NULL;
	}
	head->next = tmp;
}


int main()
{
	return 0;

}

