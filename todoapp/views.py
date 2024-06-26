from rest_framework import generics, permissions
from .models import Todo
from .serializers import TodoSerializer


class TodoListCreateView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Todo.objects.filter(user=self.request.user)
        queryset = self.filter_by_priority(queryset)
        queryset = self.filter_by_title(queryset)
        queryset = self.filter_by_date_range(queryset)
        return queryset

    def filter_by_priority(self, queryset):
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority = priority)
        return queryset

    def filter_by_title(self, queryset):
        title = self.request.query_params.get('title')
        print(title)
        if title:
            print(queryset, ' -before')
            queryset = queryset.filter(title__startswith=title)
            print(queryset, ' -before')
        return queryset

    def filter_by_date_range(self, queryset):
        date_range = self.request.query_params.get('date_range')
        if date_range:
            queryset = queryset.filter(date_range = date_range)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


import pandas as pd
from django.http import HttpResponse


class TodoDownloadView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        todos = Todo.objects.filter(user=request.user)
        data = [
            {
                "title": todo.title,
                "description": todo.description,
                "priority": todo.get_priority_display(),
            }
            for todo in todos
        ]
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="todos.csv"'
        df.to_csv(path_or_buf=response, index=False)
        return response



