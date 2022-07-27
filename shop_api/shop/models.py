from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Product(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Создатель товара.",
        related_name="product_author"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Наименование товара",
        blank=False,
        index=True
    )
    art = models.CharField(
        max_length=50,
        verbose_name="Артикул товара"
    )
    manufactorer = models.ManyToManyField(
        "Manufactorer",
        related_name="product_manufactorer",
    )
    supplier = models.ManyToManyField(
        User,
        verbose_name="Поставщик товара."
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    price = models.FloatField(
        validators=[
            MinValueValidator(1, message="Цена не может быть меньше рубля")
        ],
        verbose_name="Цена товара",
    )
    image = models.ImageField(
        verbose_name="Картинка товара",
    )
    groups = models.ForeignKey(
        "Groups",
        verbose_name="Группа товара",
        related_name="product_groups"
    )
    description: str = models.TextField(
        "Описание товара"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name


class Manufactorer(models.Model):
    name: str = models.CharField(
        max_length=255,
        verbose_name="Имя производителя",
        blank=False,
        index=True
    )
    description: str = models.TextField(
        verbose_name="Описание производителя"
    )
    image = models.ImageField(
        verbose_name="Фото производителя"
    )


class Shop_Cart(models.Model):
    pass


class Favorites(models.Model):
    pass


class Groups(models.Model):
    name: str = models.CharField(
        max_length=255,
        verbose_name="Имя группы",
        blank=False,
        index=True
    )
    slug: str = models.SlugField(
        max_length=128,
        verbose_name="Слаг группы",
        blank=False,
        index=True
    )

    def __str__(self) -> str:
        return self.name
