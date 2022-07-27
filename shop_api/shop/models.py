from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Order(models.Model):
    user = ...
    product = ...
    pass


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


class ProductMeasurement(models.Model):
    PIECE = 'Штука'
    KILOGRAM = 'Килограмм'
    GRAM = 'Грамм'
    LITRE = 'Литр'
    PACK = 'Упаковка'
    MILLILITER = 'Миллилитр'

    CHOISES = [
        (PIECE, 'шт.'),
        (KILOGRAM, 'кг.'),
        (GRAM, 'гр.'),
        (LITRE, 'л.'),
        (PACK, 'упаковка'),
        (MILLILITER, 'мл.'),
    ]
    measurement = models.CharField(
        verbose_name="Единица измерения",
        choices=CHOISES,
        blank=False
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество",
        blank=False
    )
    product = models.ForeignKey(
        "Product",
        related_name="product_measurements",
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["product", "amount"],
                                    name="unique_product_amount")
        ]

    def __str__(self) -> str:
        return f"{self.product.name}, {self.measurement}"


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

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name


class Shop_Cart(models.Model):
    user: User = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="shop_cart_user",
        on_delete=models.CASCADE
    )
    product: Product = models.ManyToManyField(
        Product,
        verbose_name="Товар",
        related_name="shop_cart_product",
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name = "Корзина"

    def __str__(self) -> str:
        return f"Корзина пользователя {self.user.username}"


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="shop_cart_user",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        related_name="shop_cart_product",
        on_delete=models.CASCADE
    )


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
