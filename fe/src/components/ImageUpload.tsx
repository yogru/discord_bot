import React, { useState } from "react";

function ImageUploadWithTagging() {
    const [selectedImage, setSelectedImage] = useState<File | null>(null); // 선택된 이미지 파일
    const [preview, setPreview] = useState<string | null>(null); // 미리보기 URL
    const [tagInput, setTagInput] = useState<string>(""); // 태그 입력값
    const [tags, setTags] = useState<string[]>([]); // Chip으로 표시될 태그 배열
    const [uploadStatus, setUploadStatus] = useState<string>(""); // 업로드 상태

    // 이미지 선택 핸들러
    function handleImageChange(event: React.ChangeEvent<HTMLInputElement>): void {
        const file = event.target.files?.[0];
        if (file) {
            setSelectedImage(file);
            setPreview(URL.createObjectURL(file)); // 미리보기 URL 생성
        }
    }

    // 태그 입력 핸들러
    function handleTagInputChange(event: React.ChangeEvent<HTMLInputElement>): void {
        setTagInput(event.target.value); // 태그 입력값 업데이트
    }

    // 태그 추가 핸들러
    function handleAddTag(event: React.KeyboardEvent<HTMLInputElement>): void {
        if (event.key === "Enter" && tagInput.trim()) {
            if (!tags.includes(tagInput.trim())) {
                setTags([...tags, tagInput.trim()]); // 태그 추가
            }
            setTagInput(""); // 입력값 초기화
        }
    }

    // 태그 삭제 핸들러
    function handleRemoveTag(tagToRemove: string): void {
        setTags(tags.filter((tag) => tag !== tagToRemove)); // 태그 삭제
    }

    // 이미지 업로드 핸들러
    async function handleUpload(): Promise<void> {
        if (!selectedImage) {
            alert("이미지를 먼저 선택하세요!");
            return;
        }

        const formData = new FormData();
        formData.append("image", selectedImage);
        formData.append("tags", tags.join(",")); // 태그 배열을 문자열로 변환하여 전송

        try {
            const response = await fetch("https://your-server-url/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                setUploadStatus("이미지 업로드 성공!");
            } else {
                setUploadStatus("이미지 업로드 실패!");
            }
        } catch (error) {
            console.error("업로드 에러:", error);
            setUploadStatus("이미지 업로드 중 오류가 발생했습니다.");
        }
    }

    return (
        <div style={{ textAlign: "center" }}>
            <h2>이미지 업로드</h2>
            <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                style={{ marginBottom: "10px" }}
            />
            {preview && (
                <div style={{ margin: "20px" }}>
                    <img
                        src={preview}
                        alt="Preview"
                        style={{ width: "300px", height: "300px", objectFit: "cover" }}
                    />
                </div>
            )}
            <div style={{ marginBottom: "10px" }}>
                <input
                    type="text"
                    placeholder="태그를 입력 후 Enter를 누르세요"
                    value={tagInput}
                    onChange={handleTagInputChange}
                    onKeyDown={handleAddTag}
                    style={{
                        padding: "5px",
                        width: "300px",
                        marginRight: "10px",
                    }}
                />
            </div>
            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    flexWrap: "wrap",
                    gap: "10px",
                    marginBottom: "20px",
                }}
            >
                {tags.map((tag, index) => (
                    <div
                        key={index}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            background: "#f0f0f0",
                            borderRadius: "20px",
                            padding: "5px 10px",
                            fontSize: "14px",
                        }}
                    >
                        <span>{tag}</span>
                        <button
                            onClick={() => handleRemoveTag(tag)}
                            style={{
                                background: "none",
                                border: "none",
                                marginLeft: "8px",
                                color: "#888",
                                cursor: "pointer",
                                fontSize: "16px",
                            }}
                        >
                            ✖
                        </button>
                    </div>
                ))}
            </div>
            <button onClick={handleUpload} style={{ padding: "10px 20px", cursor: "pointer" }}>
                업로드
            </button>
            {uploadStatus && <p>{uploadStatus}</p>}
        </div>
    );
}

export default ImageUploadWithTagging;
