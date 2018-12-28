from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User, Nutritions

engine = create_engine('sqlite:///recipes.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             photo='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Recipes for Breakfast
category1 = Category(user_id=1, title="Breakfast")

session.add(category1)
session.commit()


item1 = Item(user_id=1, title="egg", description="Juicy grilled veggie patty with tomato mayo and lettuce",
            ingredients ="jhgfkdlkgnjhlf;ds'fmkgm;d'ldsfmkglf", instructions = "fdghffgfdsadfghjfhghfds",
                        difficulty = "Easy", serves = 3,
                        preparingTime = '11', cookingTime = '60',
                       picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
                      category=category1)
item2 = Item(user_id=1, title="2", description="Juicy grilled veggie patty with tomato mayo and lettuce",
            ingredients ="jhgfkdlkgnjhlf;ds'fmkgm;d'ldsfmkglf", instructions = "fdghffgfdsadfghjfhghfds",
                        difficulty = "Easy", serves = 3,
                        preparingTime = '11', cookingTime = '60',
                       picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
                      category=category1)
session.add(item1)
session.commit()
session.add(item2)
session.commit()
nutritions1= Nutritions(item=item1,energy = '22',calories = '32',
                    fat = '44',saturatedFat = '43',
                    carbohydrate = '12',sugar = '0',
                    dietaryFiber = '12',protein = '21',
                    cholesterol = '33',sodium = '2')
nutritions2= Nutritions(item=item2,energy = '22',calories = '32',
                    fat = '44',saturatedFat = '43',
                    carbohydrate = '12',sugar = '0',
                    dietaryFiber = '12',protein = '21',
                    cholesterol = '33',sodium = '2')

session.add(nutritions1)
session.commit()
session.add(nutritions2)
session.commit()

# item2 = Item(user_id=1, title="egg", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#             ingredients ="jhgfkdlkgnjhlf;ds'fmkgm;d'ldsfmkglf", instructions = "fdghffgfdsadfghjfhghfds",
#                         difficulty = "Easy", serves = 3,
#                         preparingTime = '11', cookingTime = '60',
#                        picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
#              category=category1)

# session.add(item2)
# session.commit()

# item3 = Item(user_id=1, title="egg", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#             ingredients ="jhgfkdlkgnjhlf;ds'fmkgm;d'ldsfmkglf", instructions = "fdghffgfdsadfghjfhghfds",
#                         difficulty = "Easy", serves = 3,
#                         preparingTime = '11', cookingTime = '60',
#                        picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
#              category=category1)

# session.add(item3)
# session.commit()

# # Recipes for Lunch
# category2 = Category(user_id=1, title="Lunch")

# session.add(category2)
# session.commit()

# item1 = Item(user_id=1, title="egg", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#             ingredients ="jhgfkdlkgnjhlf;ds'fmkgm;d'ldsfmkglf", instructions = "fdghffgfdsadfghjfhghfds",
#                         difficulty = "Easy", serves = 3,
#                         preparingTime = '11', cookingTime = '60',
#                         picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
#              category=category2)

# session.add(item1)
# session.commit()


# item2 =Item(user_id=1, title="egg", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#             ingredients ="jhgfkdlkgnjhlf;ds'fmkgm;d'ldsfmkglf", instructions = "fdghffgfdsadfghjfhghfds",
#                         difficulty = "Easy", serves = 3,
#                         preparingTime = '11', cookingTime = '60',
#                         picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
#              category=category2)

# session.add(item2)
# session.commit()

# # Recipes for Dinner
# category3 = Category(user_id=1, title="Dinner")

# session.add(category3)
# session.commit()

# item1 = Item(user_id=1, title="egg", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#             ingredients ="jhgfkdlkgnjhlf;ds'fmkgm;d'ldsfmkglf", instructions = "fdghffgfdsadfghjfhghfds",
#                         difficulty = "Easy", serves = 3,
#                         preparingTime = '11', cookingTime = '60',
#                         picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png',
#              category=category3)

# session.add(item1)
# session.commit()



print "added catalog items!"