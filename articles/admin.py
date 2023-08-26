from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        if not self.forms:
            raise ValidationError('Ни одной формы не существует!')
        main_count = 0
        tags = []
        for form in self.forms:
            if not form:
                raise ValidationError('Форма не имеет заполненных полей!')
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            if form.cleaned_data['is_main']:
                main_count += 1
            tags.append(form.cleaned_data['tags'])
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if main_count > 1:
            raise ValidationError('Главной может быть только одна категория!')
        if len(set(tags)) < len(tags):
            raise ValidationError('Категории не должны повторяться!')
        if main_count < 1:
            raise ValidationError('Должна быть указана основная категория!')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 0
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

