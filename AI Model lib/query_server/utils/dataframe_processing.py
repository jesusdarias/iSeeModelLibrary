import numpy as np

def denormalize_dataframe(df,model_info):
    denorm_df=df.copy()
    column_names=list(denorm_df.columns)
    for feature in column_names:
        feature_dict=model_info["attributes"]["features"][feature]
        if(feature_dict["data_type"]=="numerical"):
            if("min" in feature_dict and "max" in feature_dict and "min_raw" in feature_dict and "max_raw" in feature_dict):
                nmin=feature_dict["min"]
                nmax=feature_dict["max"]
                min_raw=feature_dict["min_raw"]
                max_raw=feature_dict["max_raw"]
                try:
                    denorm_df[feature]=(((denorm_df[feature]-nmin)/(nmax-nmin))*(max_raw-min_raw)+min_raw)
                except:
                    raise
            elif ("mean_raw" in feature_dict and "std_raw" in feature_dict):
                mean=np.array(feature_dict["mean_raw"])
                std=np.array(feature_dict["std_raw"])
                try:
                    denorm_df[feature]=((denorm_df[feature]*std)+mean)
                except Exception as e:
                    raise
        elif feature_dict["data_type"]=="categorical":
            if("values" in feature_dict and "values_raw" in feature_dict):
                try:
                    denorm_df[feature]=feature_dict["values_raw"][int(denorm_df[feature].values[0])]
                except:
                    raise
            elif("value" in feature_dict and "ohe_feature" in feature_dict):
                if(denorm_df[feature].values[0]==0):
                    denorm_df=denorm_df.drop(feature,axis=1)
                else:
                    denorm_df[feature]=feature_dict["value"]
                    denorm_df=denorm_df.rename(columns={feature: feature_dict["ohe_feature"]})
                                        
    return denorm_df

def normalize_dict(instance,model_info):
    dictionary=instance.copy()
    column_names=list(dictionary.keys())
    for feature in column_names:
        feature_dict=model_info["attributes"]["features"][feature]
        if(feature_dict["data_type"]=="numerical"):
            if("min" in feature_dict and "max" in feature_dict and "min_raw" in feature_dict and "max_raw" in feature_dict):
                nmin=feature_dict["min"]
                nmax=feature_dict["max"]
                min_raw=feature_dict["min_raw"]
                max_raw=feature_dict["max_raw"]
                try:
                    dictionary[feature]=((dictionary[feature]-min_raw) / (max_raw - min_raw)) * (nmax - nmin) + nmin
                except:
                    raise
            elif ("mean_raw" in feature_dict and "std_raw" in feature_dict):
                mean=np.array(feature_dict["mean_raw"])
                std=np.array(feature_dict["std_raw"])
                try:
                    dictionary[feature]=((dictionary[feature]-mean)/std)
                except Exception as e:
                    raise
        elif feature_dict["data_type"]=="categorical":
            if("values" in feature_dict and "values_raw" in feature_dict):
                try:
                    dictionary[feature]=feature_dict["values_raw"][int(dictionary[feature].values[0])]
                except:
                    raise
            elif("value" in feature_dict and "ohe_feature" in feature_dict):
                if(dictionary[feature].values[0]==0):
                    dictionary=dictionary.drop(feature,axis=1)
                else:
                    dictionary[feature]=feature_dict["value"]
                    dictionary=dictionary.rename(columns={feature: feature_dict["ohe_feature"]})                           
    return dictionary