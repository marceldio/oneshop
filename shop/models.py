from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Модель категорий товаров"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """Модель подкатегорий товаров"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories",
                                 verbose_name="Родительская категория")
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    image = models.ImageField(upload_to='subcategories/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} → {self.name}"
