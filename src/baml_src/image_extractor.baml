// Extract drug information and its known side effects from a table in an image
class Drug {
    generic_name string
    brand_names string[]  @description("No special characters, only alphanumeric")
    // This entire item will only stream when complete
    @@stream.done
}

class ConditionAndDrug {
    condition string
    drug Drug[]
    side_effects string[]
}

function ExtractFromImage(img: image) -> ConditionAndDrug[] {
  client GTP4oMiniExtract
  prompt #"
    Extract the condition, drug names and side effects from the provided table with these columns:
    - Reason for drug
    - Drug names: Generic name & (Brand name)
    - Side effects


    {{ ctx.output_format }}

    {{ _.role("user") }}
    {{ img }}
  "#
}

test TestOne {
  functions [ExtractFromImage]
  args {
    img {
      file "../../data/img/drugs_1.png"
    }
  }
}

test TestTwo {
  functions [ExtractFromImage]
  args {
    img {
      file "../../data/img/drugs_2.png"
    }
  }
}
