SOCIAL_AUTH_FACEBOOK_SCOPE = [
  'email',
  ]
# don't remove, it's used by custom pipeline
SOCIAL_AUTH_FACEBOOK_FIELD_SELECTORS = [
  'picture', 'age_range', 'birthday', 'education', 'work', 'bio', 'gender', 'location',
  'link', 'verified', #'interests',
  ]
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
  ('id', 'id'),
  ('first_name', 'first_name'),
  ('last_name', 'last_name'),
  ('name', 'name'),
  ('email', 'email'),
  ('link', 'link'),

  ('gender', 'gender'),
  ('picture', 'picture'),
  ('age_range', 'age_range'),
  ('birthday', 'birthday'),
  ('education', 'education'),
  ('work', 'work'),
  ('bio', 'bio'),
  ('gender', 'gender'),
  ('location', 'location'),
  ('link', 'link'),
  ('verified', 'verified'),
  #('interests', 'interests'),
  ]
#SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}


