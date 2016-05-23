import os
import sys
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Incoming(Base):
	"""docstring for Incoming object"""

	__tablename__ = 'incoming'
	id = Column(Integer, primary_key=True)
	letter_number = Column(String(250))
	register_date = Column(String(20))
	date = Column(String(20))
	from_email = Column(String(250))
	subject = Column(String)
	file_location = Column(String)

	@property
	def serialize(self):
		# Returns object data in easily serializeable format
		return {
			'letter_number': self.letter_number,
			'register_date': self.register_date,
			'date': self.date,
			'from_email': self.from_email,
			'subject': self.subject,
			'file_location': self.file_location,
		}



class Outgoing(Base):
	"""docstring for Outgoing object"""

	__tablename__ = 'outgoing'
	id = Column(Integer, primary_key=True)
	date = Column(String(20))
	to_email = Column(String(250))
	subject = Column(String)
	file_location = Column(String)

	@property
	def serialize(self):
		# Returns object data in easily serializeable format
		return {
			'date': self.date,
			'to_email': self.to_email,
			'subject': self.subject,
			'file_location': self.file_location,
		}


engine = create_engine('postgresql://catuser:catpassword@localhost/catalogdb')
Base.metadata.create_all(engine)
