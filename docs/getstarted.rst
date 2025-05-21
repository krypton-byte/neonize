Getting Started with Neonize
===========================

What is Neonize?
--------------

Neonize is a Python library that provides an asynchronous client interface for WhatsApp messaging. It allows developers to build applications that can programmatically send and receive WhatsApp messages, handle various media types, and interact with WhatsApp features.

Installation
-----------

You can install Neonize using pip:

.. code-block:: bash

    pip install neonize

For the development version, you can install directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/krypton-byte/neonize.git

Requirements
~~~~~~~~~~~

- Python 3.10 or higher
- Async/await support

Basic Usage
----------

Here's a simple example of how to use Neonize:

.. code-block:: python

    import asyncio
    from neonize import NewAClient
    from neonize.events import MessageEv

    async def handler(client: NewAClient, message: MessageEv):
        # Get the chat and text from the message
        chat = message.Info.MessageSource.Chat
        text = message.Message.conversation
        
        # Simple ping-pong example
        if text == "ping":
            await client.send_message(chat, "pong!")

    async def main():
        # Initialize the client
        client = NewAClient()
        
        # Register the message handler
        client.register_callback(handler)
        
        # Connect and start listening
        await client.connect()
        
        # Keep the client running
        while client.connected:
            await asyncio.sleep(1)

    if __name__ == "__main__":
        asyncio.run(main())

Features
--------

Neonize supports many WhatsApp features, including:

* Sending and receiving text messages
* Handling media (images, videos, audio, documents)
* Creating and interacting with polls
* Building and sending stickers
* Message editing
* Interactive buttons and lists
* Chat settings management (muting, pinning, archiving)
* And much more!

For more detailed documentation and examples, please check the API reference and examples sections.
