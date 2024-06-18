import enum


@enum.unique
class Status(enum.Enum):
    """
    Enumerations for possible actions types for logging
    """

    PENDING = 'pending'
    COMPLETED = 'completed'


@enum.unique
class Season(enum.Enum):
    """
    Enumerations for possible actions types for logging
    """

    SPRING = 'spring'
    SUMMER = 'summer'
    FALL = 'fall'
    WINTER = 'winter'
