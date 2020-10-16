# Lint as: python3
# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Documentation control decorators."""
from typing import Callable, Iterable

_DEPRECATED = "_tf_docs_deprecated"


def set_deprecated(obj):
  """Explicitly tag an object as deprecated for the doc generator."""
  setattr(obj, _DEPRECATED, None)
  return obj


def is_deprecated(obj):
  return hasattr(obj, _DEPRECATED)


_NO_SEARCH_HINTS = "_tf_docs_no_search_hints"


def hide_from_search(obj):
  """Marks an object so metadata search hints will not be included on it's page.

  The page is set to "noindex" to hide it from search.

  Note: This only makes sense to apply to functions, classes and modules.
  Constants, and methods do not get their own pages.

  Args:
    obj: the object to hide.

  Returns:
    The object.
  """
  setattr(obj, _NO_SEARCH_HINTS, None)
  return obj


def should_hide_from_search(obj):
  """Returns true if metadata search hints should not be included."""
  return hasattr(obj, _NO_SEARCH_HINTS)


_CUSTOM_PAGE_CONTENT = "_tf_docs_custom_page_content"


def set_custom_page_content(obj, content):
  """Replace most of the generated page with custom content."""
  setattr(obj, _CUSTOM_PAGE_CONTENT, content)


def get_custom_page_content(obj):
  """Gets custom page content if available."""
  return getattr(obj, _CUSTOM_PAGE_CONTENT, None)


_DO_NOT_DOC = "_tf_docs_do_not_document"


def do_not_generate_docs(obj):
  """A decorator: Do not generate docs for this object.

  For example the following classes:

  ```
  class Parent(object):
    def method1(self):
      pass
    def method2(self):
      pass

  class Child(Parent):
    def method1(self):
      pass
    def method2(self):
      pass
  ```

  Produce the following api_docs:

  ```
  /Parent.md
    # method1
    # method2
  /Child.md
    # method1
    # method2
  ```

  This decorator allows you to skip classes or methods:

  ```
  @do_not_generate_docs
  class Parent(object):
    def method1(self):
      pass
    def method2(self):
      pass

  class Child(Parent):
    @do_not_generate_docs
    def method1(self):
      pass
    def method2(self):
      pass
  ```

  This will only produce the following docs:

  ```
  /Child.md
    # method2
  ```

  Note: This is implemented by adding a hidden attribute on the object, so it
  cannot be used on objects which do not allow new attributes to be added. So
  this decorator must go *below* `@property`, `@classmethod`,
  or `@staticmethod`:

  ```
  class Example(object):
    @property
    @do_not_generate_docs
    def x(self):
      return self._x
  ```

  Args:
    obj: The object to hide from the generated docs.

  Returns:
    obj
  """
  setattr(obj, _DO_NOT_DOC, None)
  return obj


_DO_NOT_DOC_INHERITABLE = "_tf_docs_do_not_doc_inheritable"


def do_not_doc_inheritable(obj):
  """A decorator: Do not generate docs for this method.

  This version of the decorator is "inherited" by subclasses. No docs will be
  generated for the decorated method in any subclass. Even if the sub-class
  overrides the method.

  For example, to ensure that `method1` is **never documented** use this
  decorator on the base-class:

  ```
  class Parent(object):
    @do_not_doc_inheritable
    def method1(self):
      pass
    def method2(self):
      pass

  class Child(Parent):
    def method1(self):
      pass
    def method2(self):
      pass
  ```
  This will produce the following docs:

  ```
  /Parent.md
    # method2
  /Child.md
    # method2
  ```

  When generating docs for a class's arributes, the `__mro__` is searched and
  the attribute will be skipped if this decorator is detected on the attribute
  on any class in the `__mro__`.

  Note: This is implemented by adding a hidden attribute on the object, so it
  cannot be used on objects which do not allow new attributes to be added. So
  this decorator must go *below* `@property`, `@classmethod`,
  or `@staticmethod`:

  ```
  class Example(object):
    @property
    @do_not_doc_inheritable
    def x(self):
      return self._x
  ```

  Args:
    obj: The class-attribute to hide from the generated docs.

  Returns:
    obj
  """
  setattr(obj, _DO_NOT_DOC_INHERITABLE, None)
  return obj


_FOR_SUBCLASS_IMPLEMENTERS = "_tf_docs_tools_for_subclass_implementers"


def for_subclass_implementers(obj):
  """A decorator: Only generate docs for this method in the defining class.

  Also group this method's docs with and `@abstractmethod` in the class's docs.

  No docs will generated for this class attribute in sub-classes.

  The canonical use case for this is `tf.keras.layers.Layer.call`: It's a
  public method, essential for anyone implementing a subclass, but it should
  never be called directly.

  Works on method, or other class-attributes.

  When generating docs for a class's arributes, the `__mro__` is searched and
  the attribute will be skipped if this decorator is detected on the attribute
  on any **parent** class in the `__mro__`.

  For example:

  ```
  class Parent(object):
    @for_subclass_implementers
    def method1(self):
      pass
    def method2(self):
      pass

  class Child1(Parent):
    def method1(self):
      pass
    def method2(self):
      pass

  class Child2(Parent):
    def method1(self):
      pass
    def method2(self):
      pass
  ```

  This will produce the following docs:

  ```
  /Parent.md
    # method1
    # method2
  /Child1.md
    # method2
  /Child2.md
    # method2
  ```

  Note: This is implemented by adding a hidden attribute on the object, so it
  cannot be used on objects which do not allow new attributes to be added. So
  this decorator must go *below* `@property`, `@classmethod`,
  or `@staticmethod`:

  ```
  class Example(object):
    @property
    @for_subclass_implementers
    def x(self):
      return self._x
  ```

  Args:
    obj: The class-attribute to hide from the generated docs.

  Returns:
    obj
  """
  setattr(obj, _FOR_SUBCLASS_IMPLEMENTERS, None)
  return obj


do_not_doc_in_subclasses = for_subclass_implementers


def should_skip(obj):
  """Returns true if docs generation should be skipped for this object.

  checks for the `do_not_generate_docs` or `do_not_doc_inheritable` decorators.

  Args:
    obj: The object to document, or skip.

  Returns:
    True if the object should be skipped
  """
  if isinstance(obj, type):
    # For classes, only skip if the attribute is set on _this_ class.
    if _DO_NOT_DOC in obj.__dict__:
      return True
    else:
      return False

  # Unwrap fget if the object is a property
  if isinstance(obj, property):
    obj = obj.fget

  return hasattr(obj, _DO_NOT_DOC) or hasattr(obj, _DO_NOT_DOC_INHERITABLE)


def _unwrap_func(obj):
  # Unwrap fget if the object is a property or static method or classmethod.
  if isinstance(obj, property):
    return obj.fget

  if isinstance(obj, (classmethod, staticmethod)):
    return obj.__func__

  return obj


def should_skip_class_attr(cls, name):
  """Returns true if docs should be skipped for this class attribute.

  Args:
    cls: The class the attribute belongs to.
    name: The name of the attribute.

  Returns:
    True if the attribute should be skipped.
  """
  # Get the object with standard lookup, from the nearest
  # defining parent.
  try:
    obj = getattr(cls, name)
  except AttributeError:
    # Avoid error caused by enum metaclasses in python3
    if name in ("name", "value"):
      return True
    raise

  # Unwrap fget if the object is a property
  obj = _unwrap_func(obj)

  # Skip if the object is decorated with `do_not_generate_docs` or
  # `do_not_doc_inheritable`
  if should_skip(obj):
    return True

  # Use __dict__ lookup to get the version defined in *this* class.
  obj = cls.__dict__.get(name, None)
  obj = _unwrap_func(obj)

  if obj is not None:
    # If not none, the object is defined in *this* class.
    # Do not skip if decorated with `for_subclass_implementers`.
    if hasattr(obj, _FOR_SUBCLASS_IMPLEMENTERS):
      return False

  # for each parent class
  for parent in getattr(cls, "__mro__", [])[1:]:
    obj = getattr(parent, name, None)

    if obj is None:
      continue

    obj = _unwrap_func(obj)

    # Skip if the parent's definition is decorated with `do_not_doc_inheritable`
    # or `for_subclass_implementers`
    if hasattr(obj, _DO_NOT_DOC_INHERITABLE):
      return True

    if hasattr(obj, _FOR_SUBCLASS_IMPLEMENTERS):
      return True

  # No blockng decorators --> don't skip
  return False


def decorate_all_class_attributes(decorator: Callable, cls: type,
                                  skip: Iterable[str]):
  """Applies `decorator` to every attribute defined in `cls`.

  Args:
    decorator: The decorator to apply.
    cls: The class to aply the decorator to.
    skip: A collection of attribute names that the decorator should not be
      aplied to.
  """
  skip = frozenset(skip)
  class_contents = list(cls.__dict__.items())

  for name, obj in class_contents:
    if name in skip:
      continue

    # Otherwise, exclude from documentation.
    if isinstance(obj, property):
      obj = obj.fget

    if isinstance(obj, (staticmethod, classmethod)):
      obj = obj.__func__

    try:
      decorator(obj)
    except AttributeError:
      pass
