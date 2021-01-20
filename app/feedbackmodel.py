from app import app,mysql

class newFeedback():
	def __init__(self,username=None,unitID=None,starRating=None,feedback=None,feedbackDate=None):
		self.username = username
		self.unitID = unitID
		self.feedback = feedback
		self.starRating = starRating
		self.feedbackDate = feedbackDate

	def add(self):
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO feedbacks(username,unitID,feedback,starRating,feedbackDate) VALUES (%s,%s,%s,%s,%s)",(self.username,self.unitID,self.feedback,self.starRating,self.feedbackDate))
		mysql.connection.commit()
	
	@classmethod
	def searchAllFeedback(cls,unitID):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM feedbacks WHERE unitID=%s",(unitID,))
		feedbacks = cur.fetchall()
		return feedbacks
	
	@classmethod
	def deleteFeedback(cls,feedbackNo):
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM feedbacks WHERE feedbackNo=%s",(feedbackNo,))
		mysql.connection.commit()

	@classmethod
	def updateFeedback(cls,feedback,starRating,feedbackDate,feedbackNo):
		cur = mysql.connection.cursor()
		cur.execute("UPDATE feedbacks SET feedback=%s,starRating=%s,feedbackDate=%s WHERE feedbackNo=%s",(feedback,starRating,feedbackDate,feedbackNo))
		mysql.connection.commit()

	@classmethod
	def feedbackOfTheCurrentUser(cls,username,unitID):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM feedbacks WHERE username=%s and unitID=%s",(username,unitID))
		feedback = cur.fetchall()
		return feedback

	@classmethod
	def reviewedUnitsFeedback(cls):
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM feedbacks")
		feedbacks = cur.fetchall()
		return feedbacks