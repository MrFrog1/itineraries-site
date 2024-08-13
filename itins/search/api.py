from rest_framework import viewsets
from rest_framework.response import Response
from .models import ChatMessage, ChatContext
from .serializers import ChatMessageSerializer
# import openai
from django.conf import settings

# openai.api_key = settings.OPENAI_API_KEY

class ChatViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_message = serializer.validated_data['message']

        # Retrieve relevant context
        context = ChatContext.objects.all()  # In a real scenario, you'd want to filter this based on relevance
        context_text = "\n".join([f"{c.source}: {c.content}" for c in context])

        # Prepare the prompt for the AI model
        prompt = f"""You are an AI assistant for a travel itinerary marketplace in India. 
        Use the following context to answer the user's question:

        {context_text}

        User question: {user_message}

        If you use information from the context, cite the source.
        If you don't have enough information to answer, say so politely.
        """

        # Call the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150
        )

        ai_message = response.choices[0].text.strip()

        # Save the chat message
        chat_message = ChatMessage.objects.create(
            user=request.user if request.user.is_authenticated else None,
            message=user_message,
            response=ai_message
        )

        return Response({
            'message': ai_message,
            'citation': None  # You'd need to implement logic to extract citations
        })