class Student(object):
    pass

s = Student()
s.name = 'Robi'
print(s.name)

def set_age(self, age):
    self.age = age

from types import MethodType
s.set_age = MethodType(set_age, s)
s.set_age(25)
print(s.age)

def set_score(self, score):
    self.score = score

Student.set_score = set_score

s.set_score(10)
print(s.score)


class Student(object):
    __slots__ = ('name', 'age')

s = Student()
s.name = 'Robi'
s.age = 9
#s.score = 99


class Student(object):
    def get_score(self):
        return self._score

    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an int')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100')
        self._score = value

s = Student()
s.set_score(60)
print(s.get_score())

#s.set_score(999)


class Student(object):
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an int')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100')
        self._score = value

s = Student()
s.score = 60
print(s.score)

#s.score = 999

class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2019 - self._birth


class Animal(object):
    pass

class Mammal(Animal):
    pass

class Bird(Animal):
    pass

class Dog(Mammal):
    pass

class Bat(Mammal):
    pass

class Parrot(Bird):
    pass

class Ostrich(Bird):
    pass

class Runnable(object):
    def run(self):
        print('running')

class Flyable(object):
    def fly(self):
        print('flying')

class Dog(Mammal, Runnable):
    pass

class Bat(Mammal, Flyable):
    pass

class RunnableMixIn(object):
    def run(self):
        print('running')

class FlyableMixIn(object):
    def fly(self):
        print('flying')

class Dog(Mammal, RunnableMixIn):
    pass

class Bat(Mammal, FlyableMixIn):
    pass


# __str__

class Student(object):
    def __init__(self, name):
        self.name = name

print(Student('Robi'))


class Student(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Student object (name:%s)' % self.name

print(Student('Robi'))

s = Student('Robi')
print(s)


# __iter__

class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 1000:
            raise StopIteration()
        return self.a

# for n in Fib():
#     print(n)

#Fib()[5]

# __getitem__


class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a

f = Fib()
#print(f[10])

#print(f[0:1])

class Fib(object):
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a+b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a+b
            return L

f = Fib()
#print(f[0:3])


# __getattr__

class Student(object):
    def __init__(self):
        self.name = 'Robi'


s = Student()
print(s.name)
#print(s.fix)


class Student(object):
    def __init__(self):
        self.name = 'Robi'

    def __getattr__(self, item):
        if item == 'score':
            return 99
        elif item == 'age':
            return lambda : 25


s = Student()
print(s.name)
print(s.score)
print(s.age())


class Chain(object):
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' %(self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__


print(Chain().status.user.timeline.list)


# __call__

class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, value=''):
        print('My name is %s : %s' % (self.name, value))


s = Student('Robi')
s()
s('abc')



class Chain(object):
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' %(self._path, path))

    def __call__(self, value=''):
        return Chain('%s/:%s' %(self._path, value))

    def __str__(self):
        return self._path

    __repr__ = __str__


print(Chain().users('robi').repos)


# callable()

print(callable(max))


# 枚举

from enum import Enum

Month = Enum('Month', ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dev'))
#print(Month.Jan)

for name, member in Month.__members__.items():
    print(name,'=>',member, member.value)


from enum import Enum, unique

@unique
class Weekday(Enum):
    Sun = 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6


day1 = Weekday.Mon
print(day1)
print(Weekday['Mon'])
print(Weekday.Mon.value)
print(Weekday(1))
print(Weekday(0))


class Gender(Enum):
    Male = 0
    Female = 1


class Student(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

bart = Student('Bart', Gender.Male)
if bart.gender == Gender.Male:
    print('passed')
else:
    print('failed')


# -动态语言和静态语言最大的不同，就是函数和类的定义，不是编译时定义的，而是运行时动态创建的。

class Hello(object):
    def hello(self, name='world'):
        print('Hello, %s' % name)


h = Hello()
h.hello()
print(type(Hello))
print(type(h))


# type()

def fn(self, name='world'):
    print('Hello, %s' % name)


Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
# type 三个参数: 名称, 父类集合, 方法名称与函数绑定
h = Hello()
h.hello()
print(type(Hello))
print(type(h))


# metaclass

class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)

class MyList(list, metaclass=ListMetaclass):
    pass

L = MyList()
L.add(1)
print(L)

L2 = list()
#L2.add(1)
#print(L2)


# ORM 实例

# Model, IntegerField, StringField 由框架提供

class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class IntegerField(Field):
    def __init__(self, name):
        super().__init__(name, 'bigint')


class StringField(Field):
    def __init__(self, name):
        super().__init__(name, 'varchar(100)')


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k,v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping: %s => %s' %(k,v))
                mappings[k] = v

        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k,v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))


class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')


u = User(id=123, name='Robi', email='test@a.org', password='test')
u.save()


