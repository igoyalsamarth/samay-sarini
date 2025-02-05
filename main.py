from src.optimizer import samay_sarini

# Example usage - make sure num_teachers >= num_classes

teachers = {
  "Shreyas": {
    "subjects": ["Math"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
    "Bunty": {
    "subjects": ["Math"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
    "Varun": {
    "subjects": ["Math"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Akhil": {
    "subjects": ["English"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Majit": {
    "subjects": ["English"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Vaibhav": {
    "subjects": ["English"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Rohan": {
    "subjects": ["Hindi"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Anish": {
    "subjects": ["Hindi"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Akansha": {
    "subjects": ["Hindi"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Karan": {
    "subjects": ["Physics"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Panda": {
    "subjects": ["Physics"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Dhruv": {
    "subjects": ["Physics"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Himanshi": {
    "subjects": ["Chemistry"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Arrchana": {
    "subjects": ["Chemistry"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Apporva": {
    "subjects": ["Chemistry"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Ishita": {
    "subjects": ["Biology"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Shubham": {
    "subjects": ["Biology"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Neeraj": {
    "subjects": ["Biology"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Hritik": {
    "subjects": ["Computer Science"],
    "priod_preference": [],
    "class_teacher_preference": True,
    "weekly_periods": 2,
    "common_for_all_classes": True
  },
  "Aman": {
    "subjects": ["Geography"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Kartik": {
    "subjects": ["Geography"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Rishabh": {
    "subjects": ["Geography"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Tushar": {
    "subjects": ["Civics"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Ayush": {
    "subjects": ["Civics"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Shobhit": {
    "subjects": ["Civics"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Vicky": {
    "subjects": ["History"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Sorabh": {
    "subjects": ["History"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Amit": {
    "subjects": ["History"],
    "priod_preference": [],
    "class_teacher_preference": True,
  },
  "Girraj": {
    "subjects": ["PE"],
    "priod_preference": [],
    "class_teacher_preference": False,
    "weekly_periods": 2,
    "common_for_all_classes": True
  },
  "Raj": {
    "subjects": ["Library"],
    "priod_preference": [],
    "class_teacher_preference": False,
    "weekly_periods": 1,
    "common_for_all_classes": True
  },
}

# Update for regular subjects
samay_sarini(teachers=teachers, num_classes=10, num_periods=9)

