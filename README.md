# 콘크리트 균열 검출 및 분석기

### Django, Unet, Binary Semantic Segmentation, Profiling Algorithm

### 📚 상세 내용
![image](https://user-images.githubusercontent.com/35029025/209605745-237e362f-1f80-4242-8e36-1aee696ca279.png)
![image](https://user-images.githubusercontent.com/35029025/209605857-94b51ef7-8675-485a-b66f-06d6675e22e5.png)
![image](https://user-images.githubusercontent.com/35029025/209605878-ed3210ff-f332-4505-a2ee-c04c9fdc5f2f.png)


기존 직접 자를 들고 측정했던 방식을 개선하기 위한 균열 측정 서비스입니다. 

사용자가 균열을 찍어서 서버에 올리면, Resnet 34를 백본으로 한 학습된 Unet이 균열 마스킹을 생성하고,

알고리즘으로 생성한 마스크와 AND 연산으로 합성하여 균열의 너비와 길이를 Profiling 기법으로 측정하여 결과를 사용자에게 전달합니다.

---

### 📺 시연 영상

https://www.youtube.com/watch?v=1WBm6Oe9sdw

---

### 📚 논문 보기
[논문 - 딥러닝과 이미지 처리기법을 이용한 균열 조사 방식 연구](https://file.notion.so/f/s/81644358-d9d4-45cb-aceb-0b2f5ce21721/%E1%84%83%E1%85%B5%E1%86%B8%E1%84%85%E1%85%A5%E1%84%82%E1%85%B5%E1%86%BC%E1%84%80%E1%85%AA_%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5_%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%E1%84%80%E1%85%B5%E1%84%87%E1%85%A5%E1%86%B8%E1%84%8B%E1%85%B3%E1%86%AF_%E1%84%8B%E1%85%B5%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB_%E1%84%80%E1%85%B2%E1%86%AB%E1%84%8B%E1%85%A7%E1%86%AF_%E1%84%8C%E1%85%A9%E1%84%89%E1%85%A1_%E1%84%87%E1%85%A1%E1%86%BC%E1%84%89%E1%85%B5%E1%86%A8_%E1%84%8B%E1%85%A7%E1%86%AB%E1%84%80%E1%85%AE.pdf?id=adb6cf6a-5561-4b46-b86b-dc92d6d012d6&table=block&spaceId=83eb1d63-7b45-4c5e-b0f8-52e8de274a8a&expirationTimestamp=1687608516445&signature=FZkuD3-yeICxgVhYnhKza434kHyPApyo67lOePuQlMM&downloadName=%E1%84%83%E1%85%B5%E1%86%B8%E1%84%85%E1%85%A5%E1%84%82%E1%85%B5%E1%86%BC%E1%84%80%E1%85%AA+%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5+%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%E1%84%80%E1%85%B5%E1%84%87%E1%85%A5%E1%86%B8%E1%84%8B%E1%85%B3%E1%86%AF+%E1%84%8B%E1%85%B5%E1%84%8B%E1%85%AD%E1%86%BC%E1%84%92%E1%85%A1%E1%86%AB+%E1%84%80%E1%85%B2%E1%86%AB%E1%84%8B%E1%85%A7%E1%86%AF+%E1%84%8C%E1%85%A9%E1%84%89%E1%85%A1+%E1%84%87%E1%85%A1%E1%86%BC%E1%84%89%E1%85%B5%E1%86%A8+%E1%84%8B%E1%85%A7%E1%86%AB%E1%84%80%E1%85%AE.pdf)

---
### 🏆 수상 이력

캡스톤 디자인 작품 평가 대상 수상


    
