class Student:
    
    def __init__(self,
                 scholar_id=None, apaar_id=None, permanent_enrollment_number=None,
                 name=None, class_name=None, dob=None, gender=None,
                 social_category=None, father=None, mother=None, last_school=None,
                 tc_number=None, address=None, city=None, state=None,
                 admission_date=None, contact=None, alternate_contact=None,
                 email=None, aadhaar=False, birth_certificate=False):
        
        self.scholar_id = scholar_id
        self.apaar_id = apaar_id
        self.permanent_enrollment_number = permanent_enrollment_number
        self.name = name
        self.class_name = class_name
        self.dob = dob
        self.gender = gender
        self.social_category = social_category
        self.father = father
        self.mother = mother
        self.last_school = last_school
        self.tc_number = tc_number
        self.address = address
        self.city = city
        self.state = state
        self.admission_date = admission_date
        self.contact = contact
        self.alternate_contact = alternate_contact
        self.email = email
        self.aadhaar = aadhaar
        self.birth_certificate = birth_certificate

    def to_dict(self):
        return {
            "scholar_id": self.scholar_id,
            "apaar_id": self.apaar_id,
            "permanent_enrollment_number": self.permanent_enrollment_number,
            "name": self.name,
            "class_name": self.class_name,
            "dob": self.dob,
            "gender": self.gender,
            "social_category": self.social_category,
            "father": self.father,
            "mother": self.mother,
            "last_school": self.last_school,
            "tc_number": self.tc_number,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "admission_date": self.admission_date,
            "contact": self.contact,
            "alternate_contact": self.alternate_contact,
            "email": self.email,
            "aadhaar": self.aadhaar,
            "birth_certificate": self.birth_certificate
        }

    @classmethod
    def from_dict(cls, data):

        if 'class' in data and 'class_name' not in data:
            data['class_name'] = data.pop('class')
        return cls(**data)

    def __repr__(self):
        return f"Student(scholar_id={self.scholar_id}, name='{self.name}')"