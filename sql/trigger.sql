/* 리뷰 추가할 때 검사하는 트리거 함수 */
CREATE OR REPLACE FUNCTION validate_evaluation() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM "UserEvaluation"
        WHERE store_id = New.store_id AND user_id = New.user_id
    ) THEN
        RAISE EXCEPTION '한 사용자가 같은 매장을 두 번 이상 평가할 수는 없습니다.';
    END IF;
    RETURN New;
END;
$$ LANGUAGE plpgsql;

/* Trigger 생성 */
CREATE TRIGGER t_prevent_duplicate_evaluation
BEFORE INSERT ON "UserEvaluation"
FOR EACH ROW
EXECUTE FUNCTION validate_evaluation();