-- A script that creates a stored procedure ComputeAverageScoreForUser
-- It computes and store the average score for a student.

drop procedure IF EXISTS ComputeAverageScoreForUser;
DELIMITER @@ ;
CREATE PROCEDURE ComputeAverageScoreForUser(
	IN user_id INTEGER
)
BEGIN
	UPDATE users
	SET average_score=(SELECT AVG(score) FROM corrections
				WHERE corrections.user_id=user_id)
	WHERE id=user_id;
END;@@
DELIMITER ;