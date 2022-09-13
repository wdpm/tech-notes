import random


def provide_number(min_num, max_num):
    """
    装饰器：随机生成一个在 [min_num, max_num] 范围的整数，
    并追加其为函数的第一个位置参数
    """

    def wrapper(func):
        def decorated(*args, **kwargs):
            num = random.randint(min_num, max_num)
            # 将 num 作为第一个参数追加后调用函数
            return func(num, *args, **kwargs)

        return decorated

    return wrapper

# 由于兼容类方法的问题而引入该库
import wrapt


def provide_number(min_num, max_num):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        # 参数含义：
        #
        # - wrapped：被装饰的函数或类方法
        # - instance：
        #   - 如果被装饰者为普通类方法，该值为类实例
        #   - 如果被装饰者为 classmethod 类方法，该值为类
        #   - 如果被装饰者为类/函数/静态方法，该值为 None
        #
        # - args：调用时的位置参数（注意没有 * 符号）
        # - kwargs：调用时的关键字参数（注意没有 ** 符号）
        #
        print(f'instance: {instance}')
        num = random.randint(min_num, max_num)
        # 无需关注 wrapped 是类方法或普通函数，直接在头部追加参数
        args = (num,) + args
        return wrapped(*args, **kwargs)

    return wrapper


# pure function
@provide_number(1, 100)
def print_random_number(num):
    print(num)


class Foo:
    # class instance method
    @provide_number(1, 100)
    def print_random_number(self, num):
        print(num)

    # classmethod
    @provide_number(1, 100)
    @classmethod
    def print_random_number_v2(cls, num):
        print(num)


# 输出 1-100 的随机整数
# OUTPUT: 72
print_random_number()

Foo().print_random_number()

Foo.print_random_number_v2()
