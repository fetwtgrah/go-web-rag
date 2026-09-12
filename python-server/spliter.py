def split_md(path: str):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks=[]
        current_chunks=[]
        for line in text.split("\n"):
                if line.startswith("#"):
                        if current_chunks:
                                chunks.append(
                                        "\n".join(current_chunks)
                                )
                        current_chunks=[]

                current_chunks.append(line)
        if current_chunks:
               chunks.append(
                      "\n".join(current_chunks)
               )
        result=[]
        for i,chunk in enumerate(chunks,start=1):
               item={
                      "id":i,
                      "chunk":chunk
               }
               result.append(item)
        return result
                    
#用于测试split_md   
# if __name__ == "__main__":

#     result = split_md("test.md")

#     for item in result:
#      print(item)
#      print("\n")