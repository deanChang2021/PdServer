from typing import List, Union

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser, PydanticOutputParser
from langchain_community.llms import Ollama
from pydantic import BaseModel, Field

from PdBaseKits.llm import CHAT_MODEL


class PoemInfo(BaseModel):
    bookName: str = Field(description="作者")
    authorName: str = Field(description="作者年代")
    publishDate: str = Field(description="创作时间")
    parse: str = Field(description="解读")
    prompt: List[str] = Field(description="画面描述")


class LLM:
    def chat(self, poem: str, wordSize:int):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "{parser_instructions}"),
            ("human", "请阅读这首古诗{cityName}，并给出{viewPointNum}字的介绍。")
        ])

        output_parser = CommaSeparatedListOutputParser()
        parser_instructions = output_parser.get_format_instructions()
        # 查看解析器的指令内容
        print("----- 解析器 -----")
        print(parser_instructions)

        final_prompt = prompt.invoke(
            {"cityName": poem, "viewPointNum": wordSize, "parser_instructions": parser_instructions})

        model = Ollama(model="qwen2.5")

        response = model.invoke(final_prompt)
        print("----- response -----")
        print(response)

        ret = output_parser.invoke(response)
        print("------ret-----")
        print(ret)

        return ret

    ## 输入一首诗，返回一个PoemInfo对象，或者None（失败）
    def chatPoem(self, poem : str) -> Union[PoemInfo, None]:
        outputParser = PydanticOutputParser(pydantic_object=PoemInfo)
        # 查看输出解析器的内容，会被输出成json格式
        print("----- 解析器格式 -----")
        # print(outputParser.get_format_instructions())

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{parser_instructions} 你输出的结果请使用中文。"),
            ("human",
             "你好，请你作为一个语文老师。请你帮我从下面的的文章中，提取作者、作者年代、创作时间，以及内容的详细解读，解读至少需要有200字。并根据文章的大意，制作多个画面描述提示词，我需要将画面切片描述用于midjourney生成图片。文章会被三个#符号包围。\n###{book_introduction}###")
        ])

        book_introduction = poem #"            静夜思 床前明月光，疑是地上霜，举头望明月，低头思故乡。            "

        model = Ollama(model=CHAT_MODEL)

        chain = prompt | model | outputParser
        ret : PoemInfo = chain.invoke({"book_introduction": book_introduction,
                            "parser_instructions": outputParser.get_format_instructions()})

        print("--------reg------------")
        #print(ret)
        if ret:
            return ret
        else:
            return None

if __name__ == '__main__':
    ret = LLM().chatPoem("            静夜思 床前明月光，疑是地上霜，举头望明月，低头思故乡。            ")
    print(ret.bookName)