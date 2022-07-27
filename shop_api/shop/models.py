from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Order(models.Model):
    ACCEPTED = 'Принят'
    PICKUP = 'Самовывоз'
    DELIVERY = 'Доставка'
    CANCELED = 'Отменен'
    WAIT_TO_CANCEL = 'Ожидает отмены'
    AWAIT = 'Ожидает поступления'
    GOING_TO = 'Собирается'
    REFUND = 'Возврат'

    CHOISES = [
        (ACCEPTED, 'Принят в магазине'),
        (PICKUP, 'Самовывоз'),
        (DELIVERY, 'Доставка'),
        (CANCELED, 'Отменен'),
        (WAIT_TO_CANCEL, 'Ожидает отмены'),
        (AWAIT, 'Ожидает поступления'),
        (GOING_TO, 'Собирается'),
        (REFUND, 'Возврат'),
    ]

    status: str = models.CharField(
        verbose_name="Статус заказа",
        choices=CHOISES,
        default=ACCEPTED
    )
    user = models.ForeignKey(
        User,
        related_name="order_user",
        on_delete=models.CASCADE
    )
    product = models.ManyToManyField(
        "ProductMeasurement",
        related_name="order_product",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["id"]

    def __str__(self) -> str:
        return (
            f"Заказ №{self.id}, статус: {self.status}"
        )


class Product(models.Model):
    author: User = models.ForeignKey(
        User,
        verbose_name="Создатель товара.",
        related_name="product_author"
    )
    name: str = models.CharField(
        max_length=255,
        verbose_name="Наименование товара",
        blank=False,
        index=True
    )
    art: str = models.CharField(
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
    price: float = models.ManyToManyField(
        "Price",
        verbose_name="Цена товара",
    )
    image = models.ImageField(
        verbose_name="Картинка товара",
    )
    group = models.ForeignKey(
        "Group",
        verbose_name="Группа товара",
        related_name="product_group"
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


class Price(models.Model):
    """Цена."""
    CHOISES = [
        ('RUR', 'руб.'),
        ('USD', 'дол.'),
        ('EUR', 'евр.')
    ]

    cost = models.FloatField(
        verbose_name="Цена",
        validators=[
            MinValueValidator(
                1,
                message="Цена не может быть меньше 1"
            )
        ],
        blank=False
    )
    valute = models.CharField(
        verbose_name="Валюта",
        blank=False,
        max_length=4,
        choices=CHOISES,
        default='RUR'
    )


class ProductMeasurement(models.Model):
    "Единица измерения и количество товара."
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
        (PACK, 'уп.'),
        (MILLILITER, 'мл.'),
    ]
    measurement: str = models.CharField(
        verbose_name="Единица измерения",
        choices=CHOISES,
        blank=False
    )
    amount: int = models.PositiveIntegerField(
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
        verbose_name = "Количество товара"
        verbose_name_plural = "Количество товаров"
        ordering = ["product_id"]
        constraints = [
            models.UniqueConstraint(fields=["product", "amount"],
                                    name="unique_product_amount")
        ]

    def __str__(self) -> str:
        return f"{self.product.name}, {self.measurement}"


class Manufactorer(models.Model):
    """Производитель."""
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


class ShopCart(models.Model):
    """Корзина."""
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
        verbose_name_plural = "Корзины"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["product", "user"],
                                    name="unique_product_user")
        ]

    def __str__(self) -> str:
        return f"Корзина пользователя {self.user.username}"


class Favorites(models.Model):
    "Избранные товары."
    user: User = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="shop_cart_user",
        on_delete=models.CASCADE
    )
    product: Product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        related_name="shop_cart_product",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(fields=["product", "user"],
                                    name="unique_product_user_favotite")
        ]

    def __str__(self) -> str:
        return f"{self.user.username}, {self.product.name}"


class Group(models.Model):
    """Группы товаров."""
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

    class Meta:
        verbose_name = "Группа товаров"
        verbose_name_plural = "Группы товаров"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
