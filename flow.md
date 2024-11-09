 Usage Flow
 
 Authentication (Registeration -> Login) 
 
 -> Preferences (Genre - Several songs and artists are presented to the user for them to select a fixed number. From the selections we extract genres and use this to create record in UserPreferences table) 
 
 -> Subscription (Subscribe to premium page - If closed, record is created in subscription table with free selected)

 -> User Dashboard (Displays Search field at the top. Recommendations based on previously selected genres. Recommendations are in four categories - Playlist, Radio, Podcast, Previous Searches)





# def create(self, request, *args, **kwargs):
#     serializer = self.get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     self.perform_create(serializer)
#     headers = self.get_success_headers(serializer.data)
#     user = serializer.instance
#     # token, created = Token.objects.get_or_create(user=user)
#     return Response({
#         # 'token': token.key,
#         'user': serializer.data
#     }, status=status.HTTP_201_CREATED, headers=headers)