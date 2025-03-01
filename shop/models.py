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


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="Slug")
    category = models.ForeignKey(
        "shop.Category", on_delete=models.CASCADE, related_name="products", verbose_name="Категория")
    subcategory = models.ForeignKey(
        "shop.SubCategory", on_delete=models.CASCADE, related_name="products", verbose_name="Подкатегория")
    image_small = models.ImageField(upload_to="products/small/", verbose_name="Изображение (маленькое)")
    image_medium = models.ImageField(upload_to="products/medium/", verbose_name="Изображение (среднее)")
    image_large = models.ImageField(upload_to="products/large/", verbose_name="Изображение (большое)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name
