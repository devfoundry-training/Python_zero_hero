# ============================================================
# Method Resolution Order (MRO) - The Diamond Problem
# ============================================================
# Python uses C3 Linearization to determine the order in which
# base classes are searched when calling a method.
# ============================================================
class A:
    def greet(self):
        print("Hello from A!")


class B(A):
    def greet(self):
        super().greet()  # Calls A's greet() method
        print("Hello from B!")


class C(A):
    def greet(self):
        super().greet()  # Calls A's greet() method
        print("Hello from C!")


class D(B, C):
    def greet(self):
        super().greet()  # Calls B's greet(), then C's greet(), and finally A's greet()
        print("Hello from D!")


d = D()
d.greet()  # Which greet() will be called?
print(D.mro())

# MRO determines the order in which Python searches the base classes for a method. Python uses the C3 Linearization
# algorithm to determine the MRO.
# [<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
