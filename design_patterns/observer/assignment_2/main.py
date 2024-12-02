from channel import Channel
from follower import Follower

# Instantiate a channel
channel = Channel("Tech World")

# Create followers
follower1 = Follower("Alice")
follower2 = Follower("Bob")

# Register followers to the channel
channel.registerObserver(follower1)
channel.registerObserver(follower2)

# Update the channel's status and notify followers
channel.setStatus("New video uploaded: Python Observer Pattern Explained")
channel.notifyObservers()

# Followers interact with the update
follower1.play()
follower2.play()

# Another update
channel.setStatus("Livestream started: Q&A Session")
channel.notifyObservers()

# Followers interact again
follower1.play()
follower2.play()
